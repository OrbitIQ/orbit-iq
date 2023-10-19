import './App.css'
import SatelliteTable from './components/SatelliteTable/page';

function App() {

  return (
    <>
      <div style = {{
        margin: "auto",
        width: 1600,
        paddingTop: "0.3rem"
      }}>
        <h1>Satellite Data</h1>
        <SatelliteTable/>  
      </div>
    </>
  )
}

export default App
