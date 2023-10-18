import { BrowserRouter, Route, Routes } from 'react-router-dom';
import './scss/style.scss';
import Homepage from './pages/Homepage';
import StoreKey from './pages/StoreKey';
import RetrieveKey from './pages/RetrieveKey';
import Completion from './pages/Completion';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route exact path="/store-key" element={<StoreKey />}></Route>
        <Route exact path="/retrieve-key" element={<RetrieveKey />}></Route>
        <Route exact path="/completion" element={<Completion />}></Route>
        <Route path="/" element={<Homepage />} />
      </Routes>
    </BrowserRouter>

  );
}

export default App;
