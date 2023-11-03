 import ChangelogTable from "../components/ChangelogTable/table";

function ChangelogPage() {
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
                <h1>Changelog</h1>
                <ChangelogTable />
            </div>
        </>
    )
}

export default ChangelogPage;