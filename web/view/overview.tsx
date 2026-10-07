import type { Loan, Material, Section, Summary, User } from "../model/contracts";

const statLabels: Record<string, string> = {
  materiales: "Materiales en catálogo", copias_disponibles: "Copias disponibles", usuarios: "Personas registradas",
  prestamos_activos: "Préstamos activos", prestamos_vencidos: "Préstamos vencidos",
};
export function Overview({ user, materials, loans, summary, manage, select }: {
  user: User; materials: Material[]; loans: Loan[]; summary: Summary; manage: boolean; select: (id: Section) => void;
}) {
  const active = loans.filter(loan => !loan.returnedAt);
  const stats = manage ? summary : {
    materiales: materials.length, copias_disponibles: materials.reduce((sum, item) => sum + item.availableCopies, 0),
    prestamos_activos: active.length, prestamos_vencidos: active.filter(loan => new Date(loan.dueAt) < new Date()).length,
  };
  return <>
    <section className="hero"><div className="hero-copy"><span className="hero-kicker">HOLA, {user.name.split(" ")[0]}</span>
      <h2>{manage ? <>Todo en orden.<br />Más tiempo para leer.</> : <>Tu próxima lectura<br />empieza aquí.</>}</h2>
      <p>{manage ? "Organiza tu colección, acompaña a tus lectores y sigue cada préstamo." :
        "Explora libros, revistas y tesis. Encuentra tu siguiente idea y consulta tus préstamos."}</p>
      <button className="primary" onClick={() => select("materials")}>Explorar catálogo <span aria-hidden="true">↗</span></button>
    </div><div className="book-art" aria-hidden="true"><div className="book-spine">LIBROS</div>
      <div className="book-spine">REVISTAS</div><div className="book-spine">TESIS</div><span>El conocimiento se comparte.</span></div></section>
    <div className="stats">{Object.entries(stats).map(([key, value]) => <div className="stat" key={key}>
      <span className="stat-icon" aria-hidden="true">{key === "prestamos_vencidos" ? "◷" : "↗"}</span>
      <b>{value}</b><span>{statLabels[key] ?? key}</span></div>)}</div>
    <div className="overview-grid"><section className="panel"><div className="toolbar"><div>
      <span className="section-kicker">Para tener presente</span><h2>{manage ? "Próximas devoluciones" : "Tus próximas devoluciones"}</h2>
    </div><button onClick={() => select("loans")}>Ver préstamos</button></div>
      {!active.length && <p className="empty-state">No hay préstamos pendientes de devolución.</p>}
      <ul className="activity-list">{active.slice(0, 4).map(loan => <li key={loan.id}>
        <span className="activity-icon" aria-hidden="true">▤</span><div><strong>{loan.material.title}</strong>
          <small>{manage ? loan.user.name : loan.material.type}</small></div>
        <span className={new Date(loan.dueAt) < new Date() ? "due overdue" : "due"}>
          {new Date(loan.dueAt).toLocaleDateString("es-BO", { day: "numeric", month: "short" })}
          {new Date(loan.dueAt) < new Date() && <small>Vencido</small>}</span>
      </li>)}</ul></section>
      <section className="panel collection-panel"><span className="section-kicker">Nuestra colección</span><h2>Conocimiento en cada formato</h2>
        {["libro", "revista", "tesis"].map(type => <button key={type} onClick={() => select("materials")}>
          <span>{type === "libro" ? "Libros" : type === "revista" ? "Revistas" : "Tesis"}</span>
          <b>{materials.filter(item => item.type === type).length}</b><span aria-hidden="true">↗</span></button>)}
        <p>{manage ? "Gestiona usuarios, lectores, materiales y préstamos desde el menú." :
          "Solicita tus préstamos al bibliotecario. Aquí puedes consultar disponibilidad y vencimientos."}</p>
      </section></div>
  </>;
}
