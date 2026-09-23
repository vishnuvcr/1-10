from __future__ import annotations
import argparse, json, math, re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf

@dataclass(frozen=True)
class CostModel:
    slippage_bps: float = 5.0
    brokerage_per_order: float = 20.0
    exchange_txn_rate: float = 0.0
    stt_buy_rate: float = 0.0
    stt_sell_rate: float = 0.0
    stamp_buy_rate: float = 0.0
    gst_rate: float = 0.18
    sebi_turnover_rate: float = 0.0

@dataclass
class Position:
    side: str
    entry_date: pd.Timestamp
    entry_price: float
    entry_fill: float
    stop: float
    qty: int
    entry_equity: float
    entry_cost: float

@dataclass
class Trade:
    side: str
    entry_date: str
    exit_date: str
    qty: int
    entry_price: float
    entry_fill: float
    stop: float
    exit_fill: float
    reason: str
    sma: float
    entry_equity: float
    pnl: float
    return_on_equity: float
    entry_cost: float
    exit_cost: float

def safe_name(ticker):
    return re.sub(r"[^A-Za-z0-9._-]+","_",ticker).strip("_") or "ticker"

def validate_ohlcv(df):
    if isinstance(df.columns,pd.MultiIndex):
        a=list(dict.fromkeys(df.columns.get_level_values(0)))
        df.columns=df.columns.get_level_values(0) if {"Open","High","Low","Close"} & set(a) else df.columns.get_level_values(1)
    need=["Open","High","Low","Close"]
    if any(c not in df.columns for c in need):
        raise ValueError(f"Missing OHLC columns; got {list(df.columns)}")
    cols=[c for c in ["Open","High","Low","Close","Adj Close","Volume"] if c in df.columns]
    out=df[cols].copy()
    out.index=pd.to_datetime(out.index)
    if getattr(out.index,"tz",None) is not None: out.index=out.index.tz_convert(None)
    out=out[~out.index.duplicated()].sort_index().dropna(subset=need)
    if (out.High<out.Low).any(): raise ValueError("High < Low found")
    return out

def fetch_daily_data(ticker,start,end=None,cache_dir="data/raw",refresh=False):
    cache=Path(cache_dir); cache.mkdir(parents=True,exist_ok=True)
    path=cache/f"{safe_name(ticker)}.csv"
    if path.exists() and not refresh:
        d=validate_ohlcv(pd.read_csv(path,index_col=0,parse_dates=True))
        d=d[d.index>=pd.Timestamp(start)]
        if end: d=d[d.index<pd.Timestamp(end)]
        if len(d)>=30: return d
    raw=yf.download(ticker,start=start,end=end,auto_adjust=False,progress=False,actions=False,threads=False)
    d=validate_ohlcv(raw); d.to_csv(path); return d

def rsi_wilder(close,period=14):
    delta=close.diff(); gain=delta.clip(lower=0); loss=-delta.clip(upper=0)
    ag=gain.ewm(alpha=1/period,adjust=False,min_periods=period).mean()
    al=loss.ewm(alpha=1/period,adjust=False,min_periods=period).mean()
    rs=ag/al.replace(0,np.nan); r=100-100/(1+rs)
    r=r.where(al!=0,100); return r.where(~((ag==0)&(al==0)),50)

def add_indicators(df,sma_period=21,rsi_period=14):
    d=df.copy(); d["SMA21"]=d.Close.rolling(sma_period,min_periods=sma_period).mean()
    d["PrevSMA21"]=d["SMA21"].shift(1)
    d["RSI14"]=rsi_wilder(d.Close,rsi_period); d["PrevRSI14"]=d.RSI14.shift(1); d["PrevClose"]=d.Close.shift(1)
    d["LongSignal"]=(d.PrevRSI14<10)&(d.Open<d.PrevClose)
    d["ShortSignal"]=(d.PrevRSI14>90)&(d.Open>d.PrevClose); return d

def position_size(equity,entry,stop,risk_fraction=.01,lot_size=1):
    dist=abs(entry-stop)
    if not np.isfinite(dist) or dist<=0:return 0,0.0
    risk=equity*risk_fraction; qty=int(math.floor((risk/dist)/lot_size)*lot_size); return qty,risk

def side_for_cost(side,is_entry):
    return ("BUY" if is_entry else "SELL") if side=="LONG" else ("SELL" if is_entry else "BUY")

def transaction_cost(price,qty,side,is_entry,m):
    turnover=price*qty; s=side_for_cost(side,is_entry)
    brokerage=m.brokerage_per_order; exchange=turnover*m.exchange_txn_rate
    stt=turnover*(m.stt_buy_rate if s=="BUY" else m.stt_sell_rate)
    stamp=turnover*m.stamp_buy_rate if s=="BUY" else 0.0
    sebi=turnover*m.sebi_turnover_rate; gst=m.gst_rate*(brokerage+exchange+sebi)
    return brokerage+exchange+stt+stamp+sebi+gst

def fill(price,side,is_entry,bps):
    x=bps/10000; return price*(1+x if side_for_cost(side,is_entry)=="BUY" else 1-x)

def hit_target(row,side,target):
    if not np.isfinite(target): return False,np.nan
    if side=="LONG":
        if row.Open>=target:return True,float(row.Open)
        if row.High>=target:return True,float(target)
    else:
        if row.Open<=target:return True,float(row.Open)
        if row.Low<=target:return True,float(target)
    return False,np.nan

def hit_stop(row,side,stop):
    if side=="LONG":
        if row.Open<=stop:return True,float(row.Open)
        if row.Low<=stop:return True,float(stop)
    else:
        if row.Open>=stop:return True,float(row.Open)
        if row.High>=stop:return True,float(stop)
    return False,np.nan

def close_trade(pos,raw_exit,dt,reason,sma,cash,m):
    ex=fill(raw_exit,pos.side,False,m.slippage_bps); exit_cost=transaction_cost(ex,pos.qty,pos.side,False,m)
    if pos.side=="LONG":
        cash += ex*pos.qty-exit_cost; gross=(ex-pos.entry_fill)*pos.qty
    else:
        cash -= ex*pos.qty+exit_cost; gross=(pos.entry_fill-ex)*pos.qty
    pnl=gross-pos.entry_cost; ret=pnl/pos.entry_equity if pos.entry_equity else np.nan
    tr=Trade(pos.side,str(pos.entry_date.date()),str(dt.date()),pos.qty,pos.entry_price,pos.entry_fill,pos.stop,ex,reason,float(sma),pos.entry_equity,float(pnl),float(ret),pos.entry_cost,float(exit_cost))
    return tr,cash

def metrics(trades,equity,start):
    final=float(equity.Equity.iloc[-1]); dd=equity.Equity/equity.Equity.cummax()-1
    r=equity.Equity.pct_change().fillna(0); sd=r.std(ddof=1)
    sharpe=math.sqrt(252)*r.mean()/sd if sd>0 else 0.0
    if len(trades):
        gp=float(trades.loc[trades.pnl>0,"pnl"].sum()); gl=float(-trades.loc[trades.pnl<0,"pnl"].sum())
        wr=float((trades.pnl>0).mean()); pf=gp/gl if gl>0 else math.inf; exp=float(trades.pnl.mean())
    else: gp=gl=wr=exp=pf=0.0
    return {"starting_equity":start,"final_equity":final,"final_return":final/start-1,"max_drawdown":float(dd.min()),"sharpe_ratio":float(sharpe),"trade_count":int(len(trades)),"win_rate":wr,"profit_factor":float(pf),"expectancy_per_trade":exp,"gross_profit":gp,"gross_loss":gl}

def run_backtest(df,starting_equity=100000.0,risk_fraction=.01,lot_size=1,costs=None):
    m=costs or CostModel(); d=add_indicators(df); cash=float(starting_equity); pos=None; trades=[]; eq=[]; dates=list(d.index)
    for i,dt in enumerate(dates):
        row=d.loc[dt]
        if pos is not None and i>0:
            sh,sx=hit_stop(row,pos.side,pos.stop); th,tx=hit_target(row,pos.side,row.SMA21)
            if sh and th: tr,cash=close_trade(pos,sx,dt,"STOP_SAME_BAR_CONSERVATIVE",row.SMA21,cash,m); trades.append(tr); pos=None
            elif sh: tr,cash=close_trade(pos,sx,dt,"STOP",row.SMA21,cash,m); trades.append(tr); pos=None
            elif th: tr,cash=close_trade(pos,tx,dt,"SMA_TARGET",row.SMA21,cash,m); trades.append(tr); pos=None

        if pos is None and np.isfinite(row.Open) and np.isfinite(row.SMA21):
            side=None; stop=None
            if bool(row.LongSignal): side,stop="LONG",float(row.Low)
            elif bool(row.ShortSignal): side,stop="SHORT",float(row.High)
            if side:
                qty,_=position_size(cash,float(row.Open),stop,risk_fraction,lot_size)
                if qty>0:
                    en=float(row.Open); ef=fill(en,side,True,m.slippage_bps); ec=transaction_cost(ef,qty,side,True,m); ee=float(cash)
                    cash += (-ef*qty-ec) if side=="LONG" else (ef*qty-ec)
                    pos=Position(side,dt,en,ef,stop,qty,ee,ec)
                    th,tx=hit_target(row,side,float(row.SMA21))
                    if th: tr,cash=close_trade(pos,tx,dt,"SMA_TARGET_ENTRY_DAY",row.SMA21,cash,m); trades.append(tr); pos=None
        equity=cash if pos is None else (cash+pos.qty*float(row.Close) if pos.side=="LONG" else cash-pos.qty*float(row.Close))
        eq.append({"Date":dt,"Equity":equity,"Cash":cash})
    if pos is not None:
        tr,cash=close_trade(pos,float(d.iloc[-1].Close),dates[-1],"END_OF_DATA",d.iloc[-1].SMA21,cash,m); trades.append(tr); eq[-1]["Equity"]=cash; eq[-1]["Cash"]=cash
    t=pd.DataFrame([asdict(x) for x in trades]); e=pd.DataFrame(eq).set_index("Date"); mt=metrics(t,e,starting_equity)
    mt["NON_CAUSAL_ENTRY_CANDLE_STOP"]=True; mt["cost_model"]=asdict(m); return t,e,mt

def monte_carlo_simulation(trade_returns,starting_equity=100000.0,n_sims=1000,seed=42,ruin_levels:Iterable[float]=(0.1,0.2,0.3,0.4,0.5)):
    x=np.asarray(list(trade_returns),dtype=float); x=x[np.isfinite(x)]
    if x.size==0: raise ValueError("Monte Carlo requires at least one completed trade")
    rng=np.random.default_rng(seed)
    # With-replacement bootstrap destroys historical ordering while preserving the observed trade-return distribution.
    s=rng.choice(x,size=(n_sims,x.size),replace=True)
    paths=np.empty((n_sims,x.size+1)); paths[:,0]=starting_equity; paths[:,1:]=starting_equity*np.cumprod(1+s,axis=1)
    peaks=np.maximum.accumulate(paths,axis=1); dd=paths/peaks-1; mdd=dd.min(axis=1); fr=paths[:,-1]/starting_equity-1
    summary={"n_sims":n_sims,"n_trades_per_path":int(x.size),"seed":seed,
             "final_return_percentiles":{str(p):float(np.percentile(fr,p)) for p in [5,25,50,75,95]},
             "max_drawdown_percentiles":{str(p):float(np.percentile(mdd,p)) for p in [5,25,50,75,95]},
             "risk_of_ruin":{f"{int(z*100)}%":float(np.mean(mdd<=-z)) for z in ruin_levels}}
    return pd.DataFrame({"final_return":fr,"max_drawdown":mdd}),summary,paths

def plot_monte_carlo(paths,out,start):
    fig,ax=plt.subplots(figsize=(12,7))
    for p in paths: ax.plot(p,alpha=.03,linewidth=.7)
    ax.axhline(start,ls="--",lw=1,label="Starting equity"); ax.set(xlabel="Completed trades",ylabel="Equity (INR)",title="Monte Carlo Equity Curves+§uçâçT Bootstrap With Replacement"); ax.legend(); ax.grid(alpha=.25)
    fig.tight_layout(); fig.savefig(out,dpi=160); plt.close(fig)

def vectorbt_reconciliation(data,trades,start):
    try: import vectorbt as vbt
    except Exception as exc: return {"available":False,"reason":repr(exc)}
    if trades.empty:return {"available":True,"trade_count":0}
    o=pd.DataFrame(0.0,index=data.index,columns=["size","price"])
    for _,t in trades.iterrows():
        ed,xd=pd.Timestamp(t.entry_date),pd.Timestamp(t.exit_date); q=float(t.qty)
        a,b=(q,-q) if t.side=="LONG" else (-q,q); o.loc[ed,["size","price"]]=[a,float(t.entry_fill)]; o.loc[xd,["size","price"]]=[b,float(t.exit_fill)]
    try:
        pf=vbt.Portfolio.from_orders(close=data.Close,size=o["size"],price=o.price.replace(0,np.nan),direction="both",init_cash=start,fees=0,slippage=0,freq="1D")
        return {"available":True,"final_value":float(pf.value().iloc[-1]),"total_return":float(pf.total_return())}
    except Exception as exc:return {"available":True,"reconciliation_error":repr(exc)}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--ticker",default="^NSEI"); p.add_argument("--start",default="2010-01-01"); p.add_argument("--end")
    p.add_argument("--starting-equity",type=float,default=100000); p.add_argument("--risk-fraction",type=float,default=.01); p.add_argument("--lot-size",type=int,default=1)
    p.add_argument("--n-mc",type=int,default=1000); p.add_argument("--seed",type=int,default=42); p.add_argument("--refresh-data",action="store_true")
    p.add_argument("--data-cache-dir",default="data/raw"); p.add_argument("--output-dir",default="results")
    p.add_argument("--slippage-bps",type=float,default=5); p.add_argument("--brokerage-per-order",type=float,default=20)
    p.add_argument("--exchange-txn-rate",type=float,default=0); p.add_argument("--stt-buy-rate",type=float,default=0); p.add_argument("--stt-sell-rate",type=float,default=0)
    p.add_argument("--stamp-buy-rate",type=float,default=0); p.add_argument("--gst-rate",type=float,default=.18); p.add_argument("--sebi-turnover-rate",type=float,default=0)
    a=p.parse_args(); out=Path(a.output_dir); out.mkdir(parents=True,exist_ok=True)
    c=CostModel(a.slippage_bps,a.brokerage_per_order,a.exchange_txn_rate,a.stt_buy_rate,a.stt_sell_rate,a.stamp_buy_rate,a.gst_rate,a.sebi_turnover_rate)
    data=fetch_daily_data(a.ticker,a.start,a.end,a.data_cache_dir,a.refresh_data); trades,equity,mt=run_backtest(data,a.starting_equity,a.risk_fraction,a.lot_size,c)
    if len(trades):
        dist,mc,paths=monte_carlo_simulation(trades.return_on_equity.to_numpy(),a.starting_equity,a.n_mc,a.seed); dist.to_csv(out/"monte_carlo_distribution.csv",index=False); plot_monte_carlo(paths,out/"monte_carlo_equity_curves.png",a.starting_equity)
    else: mc={"status":"not_run","reason":"No completed trades"}; paths=np.empty((0,0))
    trades.to_csv(out/"trades.csv",index=False); equity.to_csv(out/"equity_curve.csv")
    (out/"backtest_metrics.json").write_text(json.dumps(mt,indent=2,default=str)); (out/"monte_carlo_summary.json").write_text(json.dumps(mc,indent=2,default=str))
    (out/"vectorbt_reconciliation.json").write_text(json.dumps(vectorbt_reconciliation(data,trades,a.starting_equity),indent=2,default=str))
    print(json.dumps(mt,indent=2,default=str)); print(json.dumps(mc,indent=2,default=str)); print(f"Artifacts: {out.resolve()}")
    print("WARNING: entry-candle low/high sizing is NON-CAUSAL with daily OHLC; use only as a literal research specification.")

if __name__=="__main__": main()
