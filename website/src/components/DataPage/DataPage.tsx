import SatelliteTable from "../SatelliteTable/page";

function DataPage() {
    console.log("DataPage rendered!");
    
    return (
        <>
            <div
                style={{
                    margin: "auto",
                    width: 1600,
                    paddingTop: "2.3rem",
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                }}
            >
                <h1>Satellite Data</h1>
                <SatelliteTable />
            </div>
        </>
    )
}

export default DataPage;