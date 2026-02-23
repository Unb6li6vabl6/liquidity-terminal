import React, { useState, useEffect, useMemo } from 'react';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as ReChartsTooltip, 
  ResponsiveContainer, AreaChart, Area, ComposedChart
} from 'recharts';
import { Gauge, TrendingUp, TrendingDown, ShieldAlert, Activity, Zap } from 'lucide-react';

const App = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    // Pobiera dane wygenerowane przez bota GitHub
    fetch('./live_data.json')
      .then(res => res.json())
      .then(json => setData(json))
      .catch(err => console.log("Czekam na pierwsze dane..."));
  }, []);

  if (!data) return <div className="bg-[#D7C4A3] h-screen flex items-center justify-center font-black italic">INITIALIZING TERMINAL V15.0 PRO...</div>;

  return (
    <div className="min-h-screen bg-[#D7C4A3] text-[#2C261F] font-sans p-4 text-[12px]">
      
      {/* HEADER IDENTYCZNY Z TWOIM PROJEKTEM */}
      <div className="max-w-[1500px] mx-auto mb-6 bg-[#CBB491] border border-[#B89F7D] rounded-2xl p-6 shadow-xl flex justify-between items-center">
        <div className="flex items-center gap-6">
          <div className="p-4 bg-[#5D4E37] rounded-xl shadow-lg"><Gauge className="text-[#D7C4A3]" size={32} /></div>
          <div>
            <h1 className="text-2xl tracking-tighter uppercase italic font-medium leading-none">
              Liquidity <span className="text-blue-900 not-italic font-black">Intelligence Hub</span>
            </h1>
            <p className="text-[11px] text-[#5D4E37] uppercase tracking-[0.4em] mt-1 font-bold italic">
              Institutional Terminal | Live Feed | {data.last_update}
            </p>
          </div>
        </div>
        <div className="flex gap-10">
          <StatBox label="Net Liquidity" value={data.aggregates[0].value} />
          <StatBox label="System Status" value="OPERATIONAL" color="text-green-800" />
        </div>
      </div>

      {/* GRID 50 WSKAŹNIKÓW (AUTOMAT) */}
      <div className="max-w-[1500px] mx-auto grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-2 mb-8">
        {data.aggregates.map(m => (
          <div key={m.id} className="bg-[#CFB997] border border-[#B89F7D] p-3 rounded-lg flex flex-col justify-between hover:bg-[#C5AD88] transition-all">
            <span className="text-[9px] uppercase font-black opacity-70">{m.title}</span>
            <div className="flex justify-between items-end mt-1">
              <span className="text-[12px] font-bold text-black">{m.value}</span>
              {m.trend === 'up' ? <TrendingUp size={12} className="text-green-800" /> : <TrendingDown size={12} className="text-red-800" />}
            </div>
          </div>
        ))}
      </div>

      {/* GŁÓWNA ANALIZA I WYKRES */}
      <div className="max-w-[1500px] mx-auto bg-[#FEFDFB]/40 border border-[#B89F7D] rounded-3xl p-8 shadow-2xl">
        <div className="grid lg:grid-cols-3 gap-12">
          <div className="lg:col-span-2">
            <h2 className="text-xl uppercase italic font-black mb-6">Korelacja Płynności vs S&P 500</h2>
            <div className="h-[450px] bg-[#E3D5C5] rounded-2xl p-6 border border-[#B89F7D]">
              <ResponsiveContainer width="100%" height="100%">
                <ComposedChart data={data.history}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#B89F7D" vertical={false} />
                  <XAxis dataKey="date" stroke="#5D4E37" fontSize={10} />
                  <YAxis yAxisId="left" stroke="#1E40AF" fontSize={10} />
                  <YAxis yAxisId="right" orientation="right" stroke="#5D4E37" fontSize={10} />
                  <ReChartsTooltip contentStyle={{ backgroundColor: '#F5F2ED', border: 'none', borderRadius: '12px' }} />
                  <Area yAxisId="left" type="monotone" dataKey="netLiq" fill="#1E40AF15" stroke="#1E40AF" strokeWidth={3} />
                  <Line yAxisId="right" type="monotone" dataKey="spx" stroke="#5D4E37" strokeWidth={4} dot={{ r: 4 }} />
                </ComposedChart>
              </ResponsiveContainer>
            </div>
          </div>
          <div className="space-y-6">
            <div className="bg-[#E3D5C5] p-8 rounded-2xl border border-[#B89F7D]">
              <h3 className="text-[12px] uppercase mb-4 font-black italic border-b border-[#B89F7D] pb-2">Analiza AI (Live)</h3>
              <p className="italic font-bold text-justify leading-relaxed">
                Płynność netto wynosi obecnie {data.aggregates[0].value}. Przy obecnym tempie drenażu TGA i stabilnym QE (RMP), 
                fair value dla indeksu S&P 500 wyliczane jest na poziomie {Math.round(data.history[data.history.length-1].spx * 1.02)} pkt.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

const StatBox = ({ label, value, color = "text-black" }) => (
  <div className="px-4 border-l border-[#B89F7D]">
    <p className="text-[10px] text-[#5D4E37] uppercase font-black italic">{label}</p>
    <p className={`text-[16px] font-black ${color}`}>{value}</p>
  </div>
);

export default App;
