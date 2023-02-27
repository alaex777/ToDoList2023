export const postRequest = (endpoint, onLoad, onError, message) => {
    const xhr = new XMLHttpRequest()
    xhr.timeout = 1000
    xhr.open('POST', endpoint, true)
    xhr.setRequestHeader('Content-Type', 'application/json')
    xhr.onload = (e) => {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                console.log(xhr.responseText)
                console.log(JSON.parse(xhr.responseText)['message'])
                onLoad(JSON.parse(xhr.responseText)['message'])
            } else {
                console.error(xhr.status)
                onError(xhr.status)
            }
        }
    }
    xhr.ontimeout = (e) => {
        console.error('timeout')
    }
    xhr.onerror = (e) => {
        console.error(xhr.statusText)
    }
    console.log('MESSAGE: ', message)
    xhr.send(JSON.stringify(message))
}

export const getRequest = (endpoint, onLoad, onError) => {
    const xhr = new XMLHttpRequest()
    xhr.timeout = 1000
    xhr.open('GET', endpoint, true)
    xhr.onload = (e) => {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                console.log(xhr.responseText)
                onLoad(JSON.parse(xhr.responseText)['message'])
            } else {
                console.error(xhr.statusText)
                onError(xhr.status)
            }
        }
    }
    xhr.ontimeout = (e) => {
        console.error('timeout')
        onError('timeout')
    }
    xhr.onerror = (e) => {
        console.error(xhr.error)
        onError(xhr.error)
    }
    xhr.send(null)
}

export const deleteRequest = (endpoint, onError) => {
    const xhr = new XMLHttpRequest()
    xhr.timeout = 1000
    xhr.open('DELETE', endpoint, true)
    xhr.onload = (e) => {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                console.log('deletion complete')
            } else {
                console.error(xhr.statusText)
                onError(xhr.status)
            }
        }
    }
    xhr.ontimeout = (e) => {
        console.error('timeout')
        onError('timeout')
    }
    xhr.onerror = (e) => {
        console.error(xhr.error)
        onError(xhr.error)
    }
    xhr.send(null)
}