import './App.css';
import { useState } from "react";
import { Routes, Route, useRoutes } from 'react-router-dom';
import SignInPage from './pages/SignInPage';
import { Link, useNavigate } from "react-router-dom";
import NavBar from './components/navBar/NavBar';
import HomePage from './pages/HomePage';
import Chat from './pages/ChatPage'
import SignIn from './components/auth/SignIn';
import RequestAcc from './components/auth/RequestAcc'
import 'bootstrap/dist/css/bootstrap.min.css'

function App() {

  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<NavBar/>}>
          <Route index element={<HomePage />} />
          <Route path ="/chat" component ={<Chat/>}/>
        </Route>
        
        <Route path="/signin" element={<SignInPage />} />
        <Route path="/requestacc" element={<RequestAcc />} />
      </Routes>
    </div>
  )
}


export default App;
