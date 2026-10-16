import { useEffect, useMemo, useState } from "react";
import { api } from "./api";

type University = { id:number; name:string; short_name?:string; city?:string; state?:string; location?:string; type?:string; description?:string; data_status:string; source_url?:string; website?:string };
type Recommendation = { university_id:number; university:string; programme:string; location:string; nirf_rank?:number|null; naac_grade?:string|null; match_score:number; match_level:string; match_reasons:string[] };
type Resource = {id:number;title:string;resource_type:string;description?:string;source?:string;course_id:number};
type Pyq = {id:number;year:number;exam_type:string;question:string;topic?:string;marks?:number;course_id:number};
type Course = {id:number;programme_id:number;name:string;code?:string;semester?:number;credits?:number};
type Tab = "discover"|"recommend"|"compare"|"academic"|"tutor";
const tabs: {id:Tab;label:string}[]=[{id:"discover",label:"University Discovery"},{id:"recommend",label:"AI Recommendation"},{id:"compare",label:"Compare"},{id:"academic",label:"Academic Intelligence"},{id:"tutor",label:"AI Tutor"}];

export default function App(){
 const [tab,setTab]=useState<Tab>("discover");
 const [universities,setUniversities]=useState<University[]>([]);
 const [recommendations,setRecommendations]=useState<Recommendation[]>([]);
 const [selected,setSelected]=useState<number[]>([]);
 const [courses,setCourses]=useState<Course[]>([]);
 const [resources,setResources]=useState<Resource[]>([]);
 const [pyqs,setPyqs]=useState<Pyq[]>([]);
 const [stats,setStats]=useState<any>(null);
 const [loading,setLoading]=useState(false);
 const [error,setError]=useState("");
 const [query,setQuery]=useState({course:"B.Tech",branch:"Computer Science",specialization:"Data Science",location:"Lucknow",limit:"50"});
 const [question,setQuestion]=useState("Explain the difference between supervised and unsupervised learning with examples.");
 const [answer,setAnswer]=useState<any>(null);
 const [detail,setDetail]=useState<any>(null);
 const [courseFilter,setCourseFilter]=useState("");
 const [resourceFilter,setResourceFilter]=useState("all");
 const [page,setPage]=useState(0);
 const [totalLabel,setTotalLabel]=useState("");
 const [compareRows,setCompareRows]=useState<any[]>([]);
 const update=(key:keyof typeof query,value:string)=>setQuery(old=>({...old,[key]:value}));
 async function runSearch(){
  setLoading(true);setError("");setUniversities([]);setTotalLabel("");
  try{
   const p=new URLSearchParams();
   if(query.location.trim())p.set("location",query.location.trim());
   if(query.branch.trim())p.set("branch",query.branch.trim());
   if(query.course.trim())p.set("programme",query.course.trim());
   if(query.specialization.trim())p.set("specialization",query.specialization.trim());
   p.set("limit",query.limit);p.set("offset",String(page*Number(query.limit)));
   const rows=await api<University[]>(`/universities?${p.toString()}`);
   setUniversities(rows);setTotalLabel(`${rows.length} institution record(s) on this page`);
  }catch(e){setError(e instanceof Error?e.message:"Could not load institutions.");}finally{setLoading(false);}
 }
 async function runRecommendations(){
  setLoading(true);setError("");setRecommendations([]);
  try{
   const rows=await api<Recommendation[]>("/recommendations/universities",{method:"POST",body:JSON.stringify({course:query.course,branch:query.branch,specialization:query.specialization,location:query.location,prefer_nirf:true,prefer_naac:true})});
   setRecommendations(rows);if(!rows.length)setError("No verified programme records match all selected filters. Try broadening the filters or import verified programme data.");
  }catch(e){setError(e instanceof Error?e.message:"Recommendations could not be loaded.");}finally{setLoading(false);}
 }
 async function loadAcademic(){
  setLoading(true);setError("");
  try{
   const [cs,rs,ps,us,pr]=await Promise.all([api<Course[]>("/courses"),api<Resource[]>("/resources"),api<Pyq[]>("/pyqs"),api<University[]>("/universities?limit=200"),api<any[]>("/programmes")]);
   setCourses(cs);setResources(rs);setPyqs(ps);setStats({universities:us.length,programmes:pr.length,resources:rs.length,pyqs:ps.length});
  }catch(e){setError(e instanceof Error?e.message:"Academic data could not be loaded.");}finally{setLoading(false);}
 }
 async function askTutor(){
  if(!question.trim())return;
  setLoading(true);setError("");setAnswer(null);
  try{setAnswer(await api<any>("/tutor/chat",{method:"POST",body:JSON.stringify({question:question.trim()})}));}
  catch(e){setError(e instanceof Error?e.message:"Tutor request failed.");}finally{setLoading(false);}
 }
 async function showDetails(u:University){
  try{setDetail(await api<any>(`/universities/${u.id}`));}catch(e){setError(e instanceof Error?e.message:"Could not load institution details.");}
 }
 async function loadComparison(){
  if(!selected.length){setError("Add at least two institutions to compare.");return;}
  setLoading(true);setError("");
  try{setCompareRows(await Promise.all(selected.map(id=>api<any>(`/universities/${id}`))));setTab("compare");}
  catch(e){setError(e instanceof Error?e.message:"Comparison data unavailable.");}finally{setLoading(false);}
 }
 useEffect(()=>{runSearch();},[]);
 useEffect(()=>{if(tab==="academic")loadAcademic();},[tab]);
 const filteredResources=useMemo(()=>resources.filter(r=>(!courseFilter||String(r.course_id)===courseFilter)&&(resourceFilter==="all"||(r.resource_type||"").toLowerCase()===resourceFilter)),[resources,courseFilter,resourceFilter]);
 const compareItems=compareRows.length?compareRows:universities.filter(u=>selected.includes(u.id));
 function toggleSelect(id:number){setSelected(old=>old.includes(id)?old.filter(x=>x!==id):old.length<5?[...old,id]:old);}
 return <div className="app">
  <header className="topbar"><div className="brand"><div className="logo">VS</div><div><h1>VidyaSetu AI</h1><p>University Academic Intelligence & Student Success Platform</p></div></div><div className="status">Verified data • Explainable AI</div></header>
  <nav className="nav">{tabs.map(t=><button className={tab===t.id?"active":""} onClick={()=>setTab(t.id)} key={t.id}>{t.label}</button>)}</nav>
  <main>
   <section className="hero"><div><span className="pill">Student Success Platform</span><h2>Discover the right university.<br/>Then learn smarter.</h2><p>VidyaSetu AI combines university discovery, explainable recommendations, academic intelligence, PYQ insights and an educational AI tutor grounded in available sources.</p></div><div className="hero-card"><strong>Student Journey</strong><div className="journey"><span>Discover</span><b>→</b><span>Compare</span><b>→</b><span>Select</span><b>→</b><span>Learn</span><b>→</b><span>AI Support</span></div></div></section>
   {error&&<div className="notice error" role="alert">{error}<button onClick={()=>setError("")}>Dismiss</button></div>}
   {loading&&<div className="loading" role="status">Loading data from the backend…</div>}
   {(tab==="discover"||tab==="recommend")&&<section>
    <div className="section-title"><div><h3>{tab==="discover"?"Find Your University":"AI University Recommendation"}</h3><p>{tab==="discover"?"Search verified institution records by programme and location.":"Explainable preference-based matching using programme records in the database."}</p></div><button className="primary" onClick={tab==="discover"?()=>{setPage(0);runSearch();}:runRecommendations}>{tab==="discover"?"Search":"Get Recommendations"}</button></div>
    <div className="filters">
     <Field label="Course / Degree" value={query.course} onChange={v=>update("course",v)} placeholder="e.g. B.Tech"/>
     <Field label="Branch" value={query.branch} onChange={v=>update("branch",v)} placeholder="e.g. Computer Science"/>
     <Field label="Specialization" value={query.specialization} onChange={v=>update("specialization",v)} placeholder="e.g. Data Science"/>
     <Field label="Location" value={query.location} onChange={v=>update("location",v)} placeholder="City, state or region"/>
     {tab==="discover"&&<label><span>Page size</span><select value={query.limit} onChange={e=>update("limit",e.target.value)}><option value="20">20</option><option value="50">50</option><option value="100">100</option><option value="200">200</option></select></label>}
     <button className="secondary" onClick={()=>{setQuery({course:"",branch:"",specialization:"",location:"",limit:"50"});setPage(0);}}>Reset filters</button>
    </div>
    {tab==="discover"?<>
     <div className="results-meta"><span>{totalLabel}</span><span>{selected.length}/5 selected for comparison</span><button className="secondary" disabled={selected.length<2} onClick={loadComparison}>Compare selected</button></div>
     <div className="grid">{universities.map(u=><article className="card" key={u.id}><div className="card-top"><span className="tag">{u.data_status?.replaceAll("_"," ")||"DATABASE RECORD"}</span><span>{u.location||u.city||"Location unavailable"}</span></div><h4>{u.name}</h4><p>{u.description||"Institutional profile. Programme-specific availability must be confirmed from the official source."}</p><div className="facts"><span>📍 {[u.city,u.state].filter(Boolean).join(", ")||"Location not verified"}</span><span>{u.type||"Institution type unavailable"}</span></div><div className="card-actions"><button onClick={()=>toggleSelect(u.id)} className="secondary">{selected.includes(u.id)?"✓ Selected":"Add to compare"}</button><button onClick={()=>showDetails(u)}>View details</button></div>{u.website&&<a href={u.website} target="_blank" rel="noreferrer">Official website ↗</a>}</article>)}</div>
     {!universities.length&&!loading&&<div className="empty"><h4>No institution records match these filters</h4><p>Programme filters require verified programme records. Clear some filters or populate the database from official sources.</p></div>}
     <div className="pagination"><button className="secondary" disabled={page===0} onClick={()=>{setPage(p=>p-1);setTimeout(runSearch,0)}}>Previous</button><span>Page {page+1}</span><button className="secondary" disabled={universities.length<Number(query.limit)} onClick={()=>{setPage(p=>p+1);setTimeout(runSearch,0)}}>Next</button></div>
    </>:<><div className="results-meta"><span>{recommendations.length} verified programme match(es)</span><span>Maximum 100 returned per request; only matching database records are shown.</span></div><div className="grid">{recommendations.map(r=><article className="card recommendation" key={`${r.university_id}-${r.programme}`}><div className="score">{r.match_score}<small>/100</small></div><span className="tag">{r.match_level}</span><h4>{r.university}</h4><p>{r.programme}</p><div className="facts"><span>📍 {r.location}</span><span>NIRF Engineering: {r.nirf_rank??"Not verified"}</span><span>NAAC: {r.naac_grade??"Not verified"}</span></div><ul className="reasons">{r.match_reasons.map(x=><li key={x}>{x}</li>)}</ul><button onClick={()=>{toggleSelect(r.university_id);setTab("discover");}}>Add to compare</button></article>)}</div>{!recommendations.length&&!loading&&<div className="empty"><h4>No verified programme matches</h4><p>The database may contain institution ranking records but not yet have verified programme records for your exact branch and specialization.</p></div>}</>}
   </section>}
   {tab==="compare"&&<section><div className="section-title"><div><h3>University Comparison</h3><p>Compare selected institutions using sourced records. Missing values are not estimated.</p></div><button className="secondary" onClick={()=>setTab("discover")}>Choose institutions</button></div>{compareItems.length<2?<div className="empty"><h4>Select at least two institutions</h4><p>Go to University Discovery, add two to five institutions, and choose Compare selected.</p></div>:<div className="table-wrap"><table><thead><tr><th>Criteria</th>{compareItems.map((u:any)=><th key={u.id}>{u.name}</th>)}</tr></thead><tbody>{compareRow("Location",compareItems,u=>[u.city,u.state].filter(Boolean).join(", ")||"Data unavailable")}{compareRow("Institution type",compareItems,u=>u.type||"Data unavailable")}{compareRow("NIRF Engineering rank",compareItems,u=>u.ranking?.status==="VERIFIED"?`${u.ranking.rank} (${u.ranking.year})`:"Not verified")}{compareRow("NAAC grade",compareItems,u=>u.accreditation?.status==="VERIFIED"?`${u.accreditation.grade} (${u.accreditation.year})`:"Not verified")}{compareRow("Programmes",compareItems,u=>u.programmes?.map((p:any)=>p.name).join(", ")||"No verified programme records")}{compareRow("Official source",compareItems,u=>u.source_url||u.website||"Unavailable",true)}</tbody></table></div>}</section>}
   {tab==="academic"&&<section><div className="section-title"><div><h3>Academic Intelligence</h3><p>University → Programme → Semester → Course → Resources → PYQs.</p></div><button className="secondary" onClick={loadAcademic}>Refresh data</button></div><div className="grid stats">{[["Universities",stats?.universities??"—","Institution records"],["Programmes",stats?.programmes??"—","Verified programme records"],["Resources",stats?.resources??"—","Academic resource records"],["PYQs",stats?.pyqs??"—","Question-paper records"]].map(x=><article className="stat" key={x[0]}><b>{x[1]}</b><span>{x[0]}</span><small>{x[2]}</small></article>)}</div><div className="filters"><label><span>Course</span><select value={courseFilter} onChange={e=>setCourseFilter(e.target.value)}><option value="">All courses</option>{courses.map(c=><option key={c.id} value={c.id}>{c.name} {c.code?`(${c.code})`:""}</option>)}</select></label><label><span>Resource type</span><select value={resourceFilter} onChange={e=>setResourceFilter(e.target.value)}><option value="all">All types</option>{Array.from(new Set(resources.map(r=>(r.resource_type||"").toLowerCase()).filter(Boolean))).map(x=><option key={x} value={x}>{x}</option>)}</select></label></div><h4>Academic resources</h4><div className="resource-list">{filteredResources.map(r=><article className="resource" key={r.id}><div><b>{r.title||"Untitled resource"}</b><p>{r.description||"No description provided."}</p><small>{r.resource_type||"Resource"} · Course ID {r.course_id}</small></div>{r.source&&/^https?:\/\//.test(r.source)?<a href={r.source} target="_blank" rel="noreferrer">Open source ↗</a>:<span className="muted">Source unavailable</span>}</article>)}</div>{!filteredResources.length&&<div className="empty"><h4>No academic resources available</h4><p>Import actual public PDFs and official syllabus documents to populate this repository. No sample files are presented as real documents.</p></div>}<h4>Previous-year question records</h4><div className="resource-list">{pyqs.filter(p=>!courseFilter||String(p.course_id)===courseFilter).map(p=><article className="resource" key={p.id}><div><b>{p.year} · {p.exam_type}</b><p>{p.question}</p><small>{p.topic||"Topic not specified"}{p.marks?` · ${p.marks} marks`:""}</small></div></article>)}</div>{!pyqs.length&&<p className="muted">No verified PYQ records imported yet. Official question papers should be linked or stored with their source and examination year.</p>}</section>}
   {tab==="tutor"&&<section><div className="section-title"><div><h3>VidyaSetu AI Tutor</h3><p>Educational AI assistant. Live answers require a configured LLM provider.</p></div></div><div className="tutor"><label><span>Your question</span><textarea value={question} onChange={e=>setQuestion(e.target.value)} placeholder="Ask about Python, machine learning, maths, DBMS, DSA, or your syllabus…"/></label><div className="tutor-actions"><button className="primary" disabled={loading||!question.trim()} onClick={askTutor}>Ask AI Tutor</button><button className="secondary" onClick={()=>{setQuestion("");setAnswer(null);}}>New question</button></div>{answer&&<div className="answer"><div className="answer-head"><h4>Answer</h4><span className="tag">{answer.provider||"AI provider"}</span></div><p className="answer-text">{answer.answer}</p><h5>Sources from database</h5>{answer.sources?.length?answer.sources.map((s:any,i:number)=><div className="source" key={i}><b>{s.title}</b><span>{s.type} · {s.source}</span></div>):<p className="muted">No academic source documents were retrieved for this question. General explanation is not source-cited.</p>}</div>}</div><div className="notice">Setup required: add OPENAI_API_KEY to backend/.env to enable live LLM responses. Without it, the application explicitly reports that the provider is not configured.</div></section>}
  </main>
  {detail&&<div className="modal-backdrop" onClick={()=>setDetail(null)}><div className="modal" onClick={e=>e.stopPropagation()}><button className="close" onClick={()=>setDetail(null)}>×</button><span className="tag">{detail.data_status?.replaceAll("_"," ")}</span><h3>{detail.name}</h3><p>{detail.description}</p><p><b>Location:</b> {detail.city||"—"}, {detail.state||"—"}</p><p><b>Ranking:</b> {detail.ranking?.status==="VERIFIED"?`NIRF ${detail.ranking.category} ${detail.ranking.year}: ${detail.ranking.rank}`:"Not verified"}</p><p><b>Accreditation:</b> {detail.accreditation?.status==="VERIFIED"?`${detail.accreditation.grade} (${detail.accreditation.year})`:"Not verified"}</p><p><b>Source:</b> {detail.source_url||"Not available"}</p><h4>Programme records</h4>{detail.programmes?.length?detail.programmes.map((p:any)=><p key={p.id}>{p.name} · {p.branch||"Branch unavailable"} · {p.specialization||"Specialization unavailable"}</p>):<p>No verified programme records have been imported.</p>}{detail.website&&<a href={detail.website} target="_blank" rel="noreferrer">Official website ↗</a>}</div></div>}
 </div>
}
function Field({label,value,onChange,placeholder}:{label:string;value:string;onChange:(v:string)=>void;placeholder?:string}){return <label><span>{label}</span><input value={value} onChange={e=>onChange(e.target.value)} placeholder={placeholder}/></label>}
function compareRow(label:string,items:any[],value:(u:any)=>string,link=false){return <tr key={label}><th>{label}</th>{items.map((u:any)=><td key={u.id}>{link&&/^https?:\/\//.test(value(u))?<a href={value(u)} target="_blank" rel="noreferrer">Open source ↗</a>:value(u)}</td>)}</tr>}
