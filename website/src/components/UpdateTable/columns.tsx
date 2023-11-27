import { ColumnDef } from "@tanstack/react-table";
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
          cell: ({ row }: { row: Update }) => (
            <Button 
              variant={column.id === 'approve' ? 'success' : 'destructive'}
              onClick={() => column.id === 'approve' ? handleApprove(row.id) : handleDeny(row.id)}
            >
              {column.id.charAt(0).toUpperCase() + column.id.slice(1)}
            </Button>
          )
        };
      }
      return {
          ...column,
          accessorFn: row => row[column.accessorKey], 
      };
    });
  };

export default UpdateColumns;