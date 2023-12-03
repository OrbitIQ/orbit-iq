import { createContext } from 'react';
import {QueryClient} from '@tanstack/react-query';

interface QueryClientContextType {
  queryClient: QueryClient;
}

export const queryClientContext = createContext<QueryClientContextType | undefined>(undefined);
