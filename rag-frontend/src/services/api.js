import axios from "axios";
const API = axios.create({
    baseURL:"http://localhost:5000"
});
export const createSession=()=>API.post("/session");
export const getSessions=()=>API.get("/sessions");
export const getMessages = (id)=>API.get(`/messages/${id}`);
export const sendMessage=(data)=>API.post("/chat",data);