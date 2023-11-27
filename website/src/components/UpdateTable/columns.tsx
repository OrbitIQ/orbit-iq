import { ColumnDef, Row } from "@tanstack/react-table";
import { updateColumns } from "@/Constants/constants";
import { Update } from "@/types/Update";
import { Button } from "@/components/ui/button";

type HandleChangeFunction = (rowId: number) => Promise<void>;

type UpdateColumnsProps = {
  handleApprove: HandleChangeFunction;
  handleDeny: HandleChangeFunction;
};

const UpdateColumns = ({ handleApprove, handleDeny }: UpdateColumnsProps): ColumnDef<Update>[] => {
    return updateColumns.map(column => {
      if (column.id === 'approve' || column.id === 'deny') {
        return {
          ...column,
          accessorFn: row => row as Update, // this is just for type compacitity
          cell: ({ row }: { row: Row<Update> }) => (
            <Button 
              variant={column.id === 'approve' ? 'success' : 'destructive'}
              onClick={() => {
                const rowId = Number(row.original.id); // Convert to number
                return column.id === 'approve' ? handleApprove(rowId) : handleDeny(rowId);
              }}
            >
              {column.id.charAt(0).toUpperCase() + column.id.slice(1)}
            </Button>
          )
        };
      }
      return {
          ...column,
          accessorFn: row => {
            if (typeof column.accessorKey === 'string') { // Check if accessorKey is a string
              return row[column.accessorKey];
            }
            return ''; // Return a default value if accessorKey is undefined
          },
      };
    });
  };

export default UpdateColumns;