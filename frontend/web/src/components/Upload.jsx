import React, {useState} from 'react'


export default function Upload(){
const [file, setFile] = useState(null)
async function submit(e){
e.preventDefault()
const fd = new FormData()
fd.append('file', file)
const r = await fetch('/v1/uploads', {method: 'POST', body: fd})
const j = await r.json()
console.log(j)
}
return (
<form onSubmit={submit}>
<input type="file" onChange={e=>setFile(e.target.files[0])} />
<button>Upload</button>
</form>
)
}
