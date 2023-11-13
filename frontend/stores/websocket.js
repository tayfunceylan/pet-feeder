export const useWebsocketStore = defineStore("ws", () => {
  const isConnected = ref(0);
  const isLoading = ref(true);
  const firstRun = ref(true);

  const updateFunc = (msg) => {
    const meals = useMealsStore();
    const pets = usePetsStore();
    const foods = useFoodsStore();
    const schedules = useSchedulesStore();
    if (["newMeal", undefined].includes(msg)) {
      if (meals != undefined) meals.refresh();
      if (foods != undefined) foods.refresh();
    }
    if (["newPet", undefined].includes(msg))
      if (pets != undefined) pets.refresh();
    if (["newFood", undefined].includes(msg))
      if (foods != undefined) foods.refresh();
    if (["newSchedule", undefined].includes(msg))
      if (schedules != undefined) schedules.refresh();
  };
  const connectToWebsocket = (updateFunc) => {
    let protocol =
      window.location.protocol == "https:" ||
      window.location.protocol == "capacitor:"
        ? "wss"
        : "ws";
    var ws = new WebSocket(`${protocol}://${window.location.host}/ws/notify/`);

    var shouldReconnect = true;
    ws.onopen = function () {
      if (!firstRun.value) updateFunc(); // dont update on first connect
      firstRun.value = false;
      isLoading.value = false;
      isConnected.value = 100;
      console.log("WebSocket Client Connected");
    };

    ws.onmessage = function (e) {
      updateFunc(e.data);
    };

    ws.onclose = function (e) {
      isConnected.value = 0;
      if (shouldReconnect) {
        console.log(
          "Socket is closed. Reconnect will be attempted in 1 second."
        );
        setTimeout(function () {
          connectToWebsocket(updateFunc);
        }, 1000);
      }
    };

    ws.onerror = function (err) {
      console.error("Socket encountered error: Closing socket");
      ws.close();
    };
    return ws;
  };
  const ws = connectToWebsocket(updateFunc);
  return { isConnected, isLoading};
});
