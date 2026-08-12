import rawData from './data/f1-results-2016-2025.json';
import './styles.css';

type Result = {
  position: string;
  points: string;
  Driver: { givenName: string; familyName: string; code?: string };
  Constructor: { name: string };
};

type Race = {
  season: string;
  round: string;
  raceName: string;
  date: string;
  Circuit: { circuitName: string; Location: { locality: string; country: string } };
  Results: Result[];
};

const data = rawData as { range: { start: number; end: number }; source: string; fetchedAt: string; races: Race[] };

function App() {
  const races = data.races;
  const driverPoints = new Map<string, number>();
  const teamPoints = new Map<string, number>();
  const gpStarts = new Map<string, number>();
  const driverWins = new Map<string, number>();

  for (const race of races) {
    for (const result of race.Results) {
      const driver = `${result.Driver.givenName} ${result.Driver.familyName}`;
      const points = Number(result.points);
      driverPoints.set(driver, (driverPoints.get(driver) ?? 0) + points);
      teamPoints.set(result.Constructor.name, (teamPoints.get(result.Constructor.name) ?? 0) + points);
      gpStarts.set(race.raceName, (gpStarts.get(race.raceName) ?? 0) + 1);
      if (result.position === '1') driverWins.set(driver, (driverWins.get(driver) ?? 0) + 1);
    }
  }

  const topDrivers = [...driverPoints.entries()].sort((a, b) => b[1] - a[1]).slice(0, 12);
  const topTeams = [...teamPoints.entries()].sort((a, b) => b[1] - a[1]).slice(0, 10);
  const topGPs = [...gpStarts.entries()].sort((a, b) => b[1] - a[1]).slice(0, 10);
  const topWins = [...driverWins.entries()].sort((a, b) => b[1] - a[1]).slice(0, 10);

  const max = (rows: [string, number][]) => Math.max(...rows.map((r) => r[1]));

  return (
    <main className="f1-app">
      <header className="hero">
        <p className="eyebrow">Formula 1 Intelligence Dashboard</p>
        <h1>Last 10 Years of F1 Performance</h1>
        <p>
          Seasons {data.range.start}–{data.range.end} • {races.length} Grands Prix • Data source: {data.source}
        </p>
      </header>

      <section className="stats-grid">
        <StatCard label="Races analyzed" value={String(races.length)} />
        <StatCard label="Drivers with points" value={String(driverPoints.size)} />
        <StatCard label="Teams represented" value={String(teamPoints.size)} />
        <StatCard label="Data fetched" value={data.fetchedAt} />
      </section>

      <Chart title="Top Drivers by Total Points">
        <BarList rows={topDrivers} maxValue={max(topDrivers)} color="linear-gradient(90deg, #ff1801, #ffd700)" />
      </Chart>

      <Chart title="Top Teams by Total Points">
        <BarList rows={topTeams} maxValue={max(topTeams)} color="linear-gradient(90deg, #111, #666)" />
      </Chart>

      <Chart title="Most Frequently Run Grands Prix (starts logged)">
        <BarList rows={topGPs} maxValue={max(topGPs)} color="linear-gradient(90deg, #e10600, #ff6b6b)" />
      </Chart>

      <Chart title="Most Race Wins (2016–2025)">
        <BarList rows={topWins} maxValue={max(topWins)} color="linear-gradient(90deg, #d00000, #ff9500)" />
      </Chart>
    </main>
  );
}

function StatCard({ label, value }: { label: string; value: string }) {
  return (
    <article className="stat-card">
      <span>{label}</span>
      <strong>{value}</strong>
    </article>
  );
}

function Chart({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="chart">
      <h2>{title}</h2>
      {children}
    </section>
  );
}

function BarList({ rows, maxValue, color }: { rows: [string, number][]; maxValue: number; color: string }) {
  return (
    <div className="bars">
      {rows.map(([name, value]) => (
        <div key={name} className="bar-row">
          <div className="bar-label">{name}</div>
          <div className="bar-wrap">
            <div className="bar" style={{ width: `${(value / maxValue) * 100}%`, background: color }} />
            <span>{value.toFixed(1).replace('.0', '')}</span>
          </div>
        </div>
      ))}
    </div>
  );
}

export default App;
