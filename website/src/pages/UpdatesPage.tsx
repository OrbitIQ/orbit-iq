import UpdateTable from "../components/UpdateTable/UpdateTable";

function UpdatesPage() {
  return (
    <>
      {/* make title in the center */}
      <div className="flex flex-col items-center w-full max-w-7xl px-4 py-6 mx-auto sm:px-6 lg:px-8">
        <h1 className="text-3xl font-semibold text-gray-800 mb-4">
          Proposed Changes
        </h1>
        <div className="w-full overflow-x-auto">
          <UpdateTable />
        </div>
      </div>
    </>
  );
}

export default UpdatesPage;
