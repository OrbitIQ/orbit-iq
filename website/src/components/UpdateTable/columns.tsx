import { ColumnDef } from "@tanstack/react-table";
import { updateColumns } from "@/Constants/constants";
import { Update } from "@/types/Update";
import { Button } from "@/components/ui/button";

const UpdateColumns = ({ handleApprove, handleDeny }) => updateColumns.map(column => {
    if (column.id === 'approve' || column.id === 'deny') {
      return {
        ...column,
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
    return column;
  });

export default UpdateColumns;