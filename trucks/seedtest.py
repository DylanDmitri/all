import random

def router(starts, ends):


router =

'''
public class MatchingSystem : IMatchingSystem
    {
        public static Router router;
        public static IOrderManager orderManager;
        public static IDriverStatusManager driverStatusManager;


        public MatchingSystem(IOrderManager ordManager, IDriverStatusManager driManager)
        {
            orderManager = ordManager;
            driverStatusManager = driManager;
            router = MakeMatrix();
        }

        public void Main()
        {
            /*
             * get available (awaiting pickup) orders. **
             * get available truckers (available in DriverStatus). **
             * make chains of these orders per available trucker.
             * total number of truckers = total number of chains.
             * truckers that aren't available.
             */

            router = MakeMatrix();

            Chains structure = new Chains(new List<Order>(orderManager.GetAwaitingOrders()));

            int currentMin = structure.TotalFitness();
            structure.SavePotential();

            for(int i=0; i<1000; i++)
            {
                structure.Mutate();

                var thisFitness = structure.TotalFitness();

                if(structure.TotalFitness() < currentMin)
                {
                    currentMin = thisFitness;
                    structure.SavePotential();
                }
            }



             /*
              * Get all orders in transit or awaiting pickup
              * Get all available drivers
              * chains = CalcUnassignedChains(these orders, length of available drivers)
              *
              * idleDrivers = getDriverStatus where availible=true and not in workingDrivers
              * AssignIdleDrivers(chains, )
              */

        }

        public Router MakeMatrix()
        {
            List<string> driverLocs = new List<string>(driverStatusManager.GetAvailableList().Select(x => x.Location));
            List<string> orderStarts = new List<string>(orderManager.GetAwaitingOrders().Select(x => x.Start));
            List<string> orderEnds = new List<string>(orderManager.GetAllOrdersList().Where(x => x.Status != OrderStatus.Arrived).Select(x => x.End));

            var AllOrderAdresses = new string[orderStarts.Count + orderEnds.Count];
            AllOrderAdresses.CopyTo(orderStarts.ToArray(), 0);
            AllOrderAdresses.CopyTo(orderEnds.ToArray(), orderStarts.Count);

            var AllAddresses = new string[AllOrderAdresses.Length + driverLocs.Count];
            AllOrderAdresses.CopyTo(AllOrderAdresses, 0);
            AllOrderAdresses.CopyTo(driverLocs.ToArray(), AllOrderAdresses.Length);

            return new Router(AllAddresses, AllOrderAdresses);
        }


        private class Chains
        {
            List<Trucker> truckers;

            public Chains(List<Order> toAssign)
            {
                List<DriverStatus> availableTruckers = new List<DriverStatus>(driverStatusManager.GetAvailableList());

                var chains = new List<Trucker>();

                foreach(DriverStatus t in availableTruckers)
                {
                    truckers.Add(new Trucker(t));
                }


                SeedInitialCargo(toAssign, truckers);

            }

            private void SeedInitialCargo(List<Order> toAssign, List<Trucker> truckers)
            {
                int time = int.MaxValue;
                Trucker potential = null;
                foreach(Order o in toAssign)
                {
                    time = int.MaxValue;
                    foreach (Trucker trucker in truckers)
                    {
                        string truckerLoc;
                        if (trucker.PotentialEvents.Count == 0)
                        {
                            truckerLoc = trucker.status.Location;
                        }
                        else
                        {
                            truckerLoc = trucker.PotentialEvents.Last<Event>().location;
                        }

                        if (router.DistanceInSeconds(truckerLoc, o.Start) < time)
                        {
                            time = router.DistanceInSeconds(truckerLoc, o.Start);
                            potential = trucker;
                        }
                    }
                    potential.PotentialEvents.Add(new Event(pickup: true, order: o));
                    potential.PotentialEvents.Add(new Event(pickup: false, order: o));
                }
            }

            public int TotalFitness()
            {
                int total = 0;
                foreach(Trucker t in truckers)
                {
                    total += (int)Math.Pow(t.Fitness(), 2);
                }
                return total;
            }

            public void Mutate()
            {

                // generate a new PotentialEvents list for each Trucker
                // these are based on PresentEvents, but with a few attempted improvements
                // events can be switched between Truckers, then reorganized within truckers
            }

            public void SavePotential()
            {
                // for each trucker in items
                // copy the PotentialEvents into presentEvents

                foreach (Trucker t in truckers)
                {
                    t.PresentEvents = t.PotentialEvents.ConvertAll(e => new Event(pickup:e.pickup, order:e.order, inTransit:e.alreadyLoaded));
                }
            }
        }

        private class Trucker
        {
            // present are the current best that have been found
            public List<Event> PresentEvents;

            // potential are the ones being tested this round
            public List<Event> PotentialEvents;

            public List<Order> inTruck;
            public DriverStatus status;

            public Trucker(DriverStatus basis)
            {

                status = basis;

                foreach (Order o in MatchingSystem.orderManager.GetInTransitOrders())
                {
                    if (o.Trucker == status.Trucker)
                    {
                        inTruck.Add(o);
                        PresentEvents.Add(new Event(pickup:true, order:o, inTransit:true));
                    }
                }
            }

            public int Fitness()
            {
                List<string> addresses = new List<string> { status.Location };

                foreach (Event e in PotentialEvents)
                {
                    addresses.Add(e.location);
                }

                int total = 0;
                for(int i = 0; i < addresses.Count-2; i++)
                {
                    total += MatchingSystem.router.DistanceInSeconds(addresses[i], addresses[i + 1]);
                }
                return total;
            }
        }


		private class Event
        {
            public bool pickup;
            public bool alreadyLoaded;
            public string location;
            public Order order;

            public Event(bool pickup, Order order, bool inTransit = false)
            {
                this.pickup = pickup;
                this.order = order;
                this.alreadyLoaded = inTransit;

                if (pickup)
                {
                    location = order.Start;
                }
                else
                {
                    location = order.End;
                }
            }
        }

'''