export const useWebsocketStore = defineStore("ws", () => {
  const isConnected = ref(0);
  const isLoading = ref(true);
  const firstRun = ref(true);
  const wsIsConnecting = ref(false);
  const meals = useMealsStore();
  const pets = usePetsStore();
  const foods = useFoodsStore();
  const schedules = useSchedulesStore();

  const updateFunc = (msg) => {
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

  const ws = ref();

  const wsURL = `${
    ["https:", "capacitor:"].includes(window.location.protocol) ? "wss" : "ws"
  }://${window.location.host}/ws/notify/`;

  const connectToWebsocket = () => {
    if (wsIsConnecting.value) return;
    if(ws.value) ws.value.close()
    isConnected.value = 0
    isLoading.value = true
    wsIsConnecting.value = true
    const websocket = new WebSocket(wsURL);

    var shouldReconnect = true;
    websocket.onopen = function () {
      if (!firstRun.value) updateFunc(); // dont update on first connect
      firstRun.value = false;
      isLoading.value = false;
      isConnected.value = 100;
      console.log("WebSocket Client Connected");
    };

    websocket.onmessage = function (e) {
      updateFunc(e.data);
    };

    websocket.onclose = function (e) {
      isConnected.value = 0;
      wsIsConnecting.value = false;
      if (shouldReconnect) {
        console.log(
          "Socket is closed. Reconnect will be attempted in 1 second."
        );
        setTimeout(connectToWebsocket, 1000);
      }
    };

    websocket.onerror = function (err) {
      console.error("Socket encountered error: Closing socket");
      ws.close();
    };
    ws.value = websocket;
  };
  
  const addOnForegroundListener = () => {
    document.addEventListener("visibilitychange", () => {
      if (document.visibilityState === "visible") {
        connectToWebsocket()
        setTimeout(connectToWebsocket, 100);
        setTimeout(connectToWebsocket, 500);
      }
    });
  };
  
  const init = function (){
    connectToWebsocket()
    addOnForegroundListener()
  }()

  return { ws, isConnected, isLoading };
});
