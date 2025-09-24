import React, {useEffect, useRef} from 'react'
import * as pdfjsLib from 'pdfjs-dist'


pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://unpkg.com/pdfjs-dist@3.7.107/build/pdf.worker.min.js'


export default function Viewer({url}){
const canvasRef = useRef()
useEffect(()=>{
async function render(){
const loadingTask = pdfjsLib.getDocument(url)
const pdf = await loadingTask.promise
const page = await pdf.getPage(1)
const viewport = page.getViewport({scale: 1.5})
const canvas = canvasRef.current
canvas.width = viewport.width
canvas.height = viewport.height
const ctx = canvas.getContext('2d')
await page.render({canvasContext: ctx, viewport}).promise
}
if(url) render()
}, [url])
return <canvas ref={canvasRef}></canvas>
}
