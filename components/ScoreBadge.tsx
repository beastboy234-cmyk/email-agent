export function ScoreBadge({ score }: { score: number }) {
  const color = score >= 90 ? "bg-mission" : score >= 80 ? "bg-navy" : "bg-amber-600";
  return <div className={`flex h-24 w-24 shrink-0 flex-col items-center justify-center rounded-3xl ${color} text-white shadow-lg`}><span className="text-3xl font-black">{score}</span><span className="text-center text-[10px] font-bold uppercase leading-tight tracking-wide">Mission<br />Ready Score</span></div>;
}
