import ChangelogTable from "../components/ChangelogTable/changelog-table";

function ChangelogPage() {
  return (
    <div className="flex flex-col items-center w-full max-w-7xl px-4 py-6 mx-auto sm:px-6 lg:px-8">
      <h1 className="text-3xl font-semibold text-gray-800 mb-4">Verified Data Changelog</h1>
      <div className="w-full overflow-x-auto">
        <ChangelogTable />
      </div>
    </div>
  );
}

export default ChangelogPage;
