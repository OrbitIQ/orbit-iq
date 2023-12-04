import { ColumnDef, Row } from "@tanstack/react-table";
import { updateColumns } from "@/Constants/constants";
import { Update } from "@/types/Update";
import { Button } from "@/components/ui/button";

type HandleChangeFunction = (rowId: number) => Promise<void>;

type UpdateColumnsProps = {
  handleApprove: HandleChangeFunction;
  handleDeny: HandleChangeFunction;
  handleToggleStatus: HandleChangeFunction;
};

const UpdateColumns = ({ handleApprove, handleDeny, handleToggleStatus }: UpdateColumnsProps): ColumnDef<Update>[] => {
  return [
    ...updateColumns.map(column => {
      if (column.id === 'approve' || column.id === 'deny') {
        return {
          ...column,
          accessorFn: (row: Update)  => row as Update,
          cell: ({ row }: { row: Row<Update> }) => {
            const isApproved = row.original.is_approved === 'approved';
            const isDenied = row.original.is_approved === 'denied';

            return (
              <div>
                <Button 
                  variant={column.id === 'approve' ? 'success' : 'destructive'}
                  onClick={() => {
                    const rowId = Number(row.original.id);
                    return column.id === 'approve' ? handleApprove(rowId) : handleDeny(rowId);
                  }}
                  disabled={isApproved || isDenied} // Disable button if the row is approved or denied
                >
                  {column.id.charAt(0).toUpperCase() + column.id.slice(1)}
                </Button>
              </div>
            );
          }
        };
      }
      return column;
    }),
    {
      id: 'toggleStatus',
      header: 'More Action',
      cell: ({ row }: { row: Row<Update> }) => {
        const isDenied = row.original.is_approved === 'denied';
        return (
          <div>
            {isDenied && (
              <Button
                onClick={() => handleToggleStatus(Number(row.original.id))}
                variant="default"
              >
                Undo Deny
              </Button>
            )}
          </div>
        );
      }
    }
  ];
};

export default UpdateColumns;
