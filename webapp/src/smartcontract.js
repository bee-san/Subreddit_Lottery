import { ethers, utils } from "ethers";
import abi from './utils/WinnerPicker.json'

export default function SmartContract(){
    const contractAddress = "0xf114eE92b1Fd37642D573fd0CEC82aF1532cCD18 ";
    const contractABI = abi.abi;

    const winnerPicker = async () => {
      try {
        const { ethereum } = window;
  
        if (ethereum) {
          const provider = new ethers.providers.Web3Provider(ethereum);
          const signer = provider.getSigner();
  
          /*
          * You're using contractABI here
          */
          const winnerPicker = new ethers.Contract(contractAddress, contractABI, signer);
          console.log("i get to after winnerPicker");
          const cars = ["Saab", "Volvo", "BMW"];
          let count = await winnerPicker.pickWinners(1, cars);
          console.log("Retrieved total wave count...", count);
        } else {
          console.log("Ethereum object doesn't exist!");
        }
      } catch (error) {
        console.log(error)
      }
    }
  return (
    <div>
      <button className="winnerPicker" onClick={winnerPicker}>
      Pick Winners
      </button>
    </div>
  )
}