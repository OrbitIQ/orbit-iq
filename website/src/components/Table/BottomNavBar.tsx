import { Button } from "@/components/ui/button";

export default function BottomNavBar({handlePreviousPage, handleNextPage}: {handlePreviousPage: () => void, handleNextPage: ()=> void}){
    return(

        <div className="flex items-center justify-end space-x-2 py-4">
          <Button
            variant="outline"
            buttonSize="sm"
            onClick={handlePreviousPage}
          >
            Previous
          </Button>
          <Button
            variant="outline"
            buttonSize="sm"
            onClick={handleNextPage}
          >
            Next
          </Button>
        </div>
    )
}