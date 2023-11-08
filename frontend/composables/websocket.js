export const useLoading = () => useState('isLoading', () => true)
export const useConnected = () =>  useState('isConnected', () => 0)

export const connectToWebsocket = async (updateFunc) => {
    let protocol = window.location.protocol == 'https:' || window.location.protocol == 'capacitor:' ? 'wss' : 'ws'
    var ws = new WebSocket(`${protocol}://${window.location.host}/ws/notify/`)

    console.log(window.location)
    const isConnected = useConnected()
    const isLoading = useLoading()
    var shouldReconnect = true
    ws.onopen = function() {
        if (isConnected.value != 0) updateFunc() // dont update on first connect
        isLoading.value = false
        isConnected.value = 100
        console.log('WebSocket Client Connected')
    }
  
    ws.onmessage = function(e) { 
        updateFunc(e.data)
    }
  
    ws.onclose = function(e) {
        isConnected.value = 0
        if(shouldReconnect){
            console.log('Socket is closed. Reconnect will be attempted in 1 second.');
            setTimeout(function() { connectToWebsocket(updateFunc) }, 1000)
        }
    }
  
    ws.onerror = function(err) {
      console.error('Socket encountered error: Closing socket')
      ws.close()
    }
    ws.customClose = function() {
        shouldReconnect = false
        ws.close()
    }
    return ws
}