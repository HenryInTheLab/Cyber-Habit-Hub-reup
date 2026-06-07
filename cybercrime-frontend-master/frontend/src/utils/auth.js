// 认证工具函数

// JWT token解析函数
function parseJWT(token) {
  try {
    const base64Url = token.split('.')[1]
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
    const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
      return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)
    }).join(''))
    return JSON.parse(jsonPayload)
  } catch (error) {
    console.error('Error parsing JWT:', error)
    return null
  }
}

// 检查token是否过期
function isTokenExpired(token) {
  if (!token) return true

  const payload = parseJWT(token)
  if (!payload || !payload.exp) return true

  const currentTime = Math.floor(Date.now() / 1000)
  return payload.exp < currentTime
}

// 自动登出函数
function autoLogout() {
  try {
    // 清除所有认证相关的localStorage
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user_info')

    // 使用路由跳转而不是页面刷新
    if (window.location.pathname !== '/signin') {
      window.location.href = '/signin'
    }

    console.log('User automatically logged out due to token expiration')
  } catch (error) {
    console.error('Error during auto logout:', error)
    // 如果出错，至少清除localStorage
    localStorage.clear()
    if (window.location.pathname !== '/signin') {
      window.location.href = '/signin'
    }
  }
}

// 检查并处理token过期
export function checkTokenExpiration() {
  const accessToken = localStorage.getItem('access_token')
  const refreshToken = localStorage.getItem('refresh_token')

  // 如果没有token，说明用户未登录，不需要检查
  if (!accessToken && !refreshToken) {
    return true
  }

  let accessTokenExpired = false
  let refreshTokenExpired = false

  // 检查access token是否过期
  if (accessToken && isTokenExpired(accessToken)) {
    accessTokenExpired = true
    // 立即删除过期的access token
    localStorage.removeItem('access_token')
    console.log('Access token expired and removed')
  }

  // 检查refresh token是否过期
  if (refreshToken && isTokenExpired(refreshToken)) {
    refreshTokenExpired = true
    // 立即删除过期的refresh token
    localStorage.removeItem('refresh_token')
    console.log('Refresh token expired and removed')
  }

  // 如果两个token都过期了，自动登出
  if (accessTokenExpired && refreshTokenExpired) {
    // 删除用户信息
    localStorage.removeItem('user_info')
    autoLogout()
    return false
  }

  // 如果access token过期但refresh token还有效，可以尝试刷新
  if (accessTokenExpired && !refreshTokenExpired) {
    console.log('Access token expired, refresh token still valid')
    // 这里可以添加token刷新逻辑
    // 暂时先登出，后续可以实现token刷新
    localStorage.removeItem('user_info')
    autoLogout()
    return false
  }

  return true
}

// 获取有效的access token
export function getValidAccessToken() {
  const accessToken = localStorage.getItem('access_token')

  // 如果没有access token，直接返回null（用户未登录）
  if (!accessToken) {
    return null
  }

  // 如果access token过期
  if (isTokenExpired(accessToken)) {
    // 立即删除过期的access token
    localStorage.removeItem('access_token')
    console.log('Expired access token removed in getValidAccessToken')

    // 检查refresh token
    const refreshToken = localStorage.getItem('refresh_token')
    if (!refreshToken || isTokenExpired(refreshToken)) {
      // 如果refresh token也过期，删除并登出
      if (refreshToken) {
        localStorage.removeItem('refresh_token')
        console.log('Expired refresh token removed in getValidAccessToken')
      }
      localStorage.removeItem('user_info')
      autoLogout()
      return null
    }

    // 如果refresh token有效但access token过期，暂时登出
    // 后续可以实现token刷新逻辑
    localStorage.removeItem('user_info')
    autoLogout()
    return null
  }

  return accessToken
}

// 设置定时检查token过期
let tokenCheckInterval = null

export function startTokenExpirationCheck() {
  // 清除现有的定时器
  if (tokenCheckInterval) {
    clearInterval(tokenCheckInterval)
  }

  // 立即检查一次
  checkTokenExpiration()

  // 每30秒检查一次token过期
  tokenCheckInterval = setInterval(() => {
    checkTokenExpiration()
  }, 30000) // 30秒
}

export function stopTokenExpirationCheck() {
  if (tokenCheckInterval) {
    clearInterval(tokenCheckInterval)
    tokenCheckInterval = null
  }
}

// 在API请求前检查token
export function checkTokenBeforeRequest() {
  return checkTokenExpiration()
}
