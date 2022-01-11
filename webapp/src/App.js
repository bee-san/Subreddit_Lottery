import logo from './logo.svg';
import './App.css';
import Wallet from './wallet'
import SmartContract from './smartcontract'

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
          <Wallet />
          < SmartContract />
          Learn React
      </header>
    </div>
  );
}

export default App;
