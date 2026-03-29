import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export const useTransportStore = create(
  persist(
    (set) => ({
      currentUser: null, // { role: 'owner' | 'driver', name: '...', email: '...' }
      loginUser: (user) => set({ currentUser: user }),
      logoutUser: () => set({ currentUser: null }),
      
      // Drivers state
      drivers: [
        { id: 1, name: 'Gopi', email: 'gopi.@gmail.com', license: 'AG-773X', status: 'Available', currentAssignment: null },
        { id: 2, name: 'Manoj', email: 'manoj.@gmail.com', license: 'AG-918Z', status: 'Available', currentAssignment: null },
        { id: 3, name: 'Magesh', email: 'magesh.@gmail.com', license: 'AG-244B', status: 'Assigned', 
          currentAssignment: { id: 101, customerName: 'Sarah Jenkins', email: 'sarah.j@corp.com', destination: 'Orbital Sector 4' } },
        { id: 4, name: 'Ramesh', email: 'ramesh.@gmail.com', license: 'AG-505V', status: 'Available', currentAssignment: null },
      ],

      // Actions
      assignRide: (driverId, assignment) => 
        set((state) => ({
          drivers: state.drivers.map(driver => 
            driver.id === driverId 
              ? { ...driver, status: 'Assigned', currentAssignment: assignment }
              : driver
          )
        })),

      acceptRide: (driverId) =>
        set((state) => ({
          drivers: state.drivers.map(driver =>
            driver.id === driverId
              ? { ...driver, status: 'Accepted' }
              : driver
          )
        })),

      declineRide: (driverId, reason) =>
        set((state) => ({
          drivers: state.drivers.map(driver =>
            driver.id === driverId
              ? { ...driver, status: 'Declined', declineReason: reason }
              : driver
          )
        })),
        
      clearAssignment: (driverId) =>
        set((state) => ({
          drivers: state.drivers.map(driver =>
            driver.id === driverId
              ? { ...driver, status: 'Available', currentAssignment: null, declineReason: null }
              : driver
          )
        })),
    }),
    {
      name: 'vellore-transport-storage',
    }
  )
);
