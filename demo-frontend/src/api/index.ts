// index.ts
import axios, { type AxiosRequestConfig, type Method } from "axios";
import router from "@/router";
import { ElMessage } from "element-plus";
// import { tokenStore } from "@/stores/token";

/**
 * 请求失败后的错误统一处理
 * @param {Number} status 请求失败的状态码
 */
const errorHandle = (status: number, other: string) => {
  // 状态码判断
  switch (status) {
    case 302:
      ElMessage.error("接口重定向了！");
      break;
    case 400:
      ElMessage.error(
        "发出的请求有错误，服务器没有进行新建或修改数据的操作==>"
      );
      break;
    // 401: 未登录
    // 未登录则跳转登录页面，并携带当前页面的路径
    // 在登录成功后返回当前页面，这一步需要在登录页操作。
    case 401: //重定向
      ElMessage.info("请登录！若无账号请联系管理员^^");
      // tokenStore().changeToken("");
      router.replace({
        path: "/foradminlogin",
      });
      break;
    // 403 token过期
    // 清除token并跳转登录页
    case 403:
      ElMessage.warning("您没有权限进行此操作/浏览！" + other);
      // router.replace({
      //   path: "/errorUnauthorized",
      // });
      // store.commit('token', null);
      // tokenStore().changeToken("");
      // setTimeout(() => {
      //   router.replace({
      //     path: "/ssologin",
      //   });
      // }, 1000);
      break;
    case 404:
      ElMessage.error("网络请求不存在");
      router.replace({
        path: "/errorNotFound",
      });
      break;
    case 406:
      ElMessage.error("请求的格式不可得");
      break;
    case 408:
      ElMessage.error(" 请求超时！");
      break;
    case 410:
      ElMessage.error("请求的资源被永久删除，且不会再得到的");
      break;
    case 422:
      ElMessage.error("当创建一个对象时，发生一个验证错误");
      break;
    case 500:
      ElMessage.error("服务器发生错误，请检查服务器");
      break;
    case 502:
      ElMessage.error("网关错误");
      break;
    case 503:
      ElMessage.error("服务不可用，服务器暂时过载或维护");
      break;
    case 504:
      ElMessage.error("网关超时");
      break;
    default:
      ElMessage.error("其他错误" + other);
  }
};

// 定义接口
interface PendingType {
  url?: string;
  method?: Method;
  params: unknown;
  data: unknown;
  cancel: unknown;
}
// 取消重复请求
const pending: Array<PendingType> = [];
const CancelToken = axios.CancelToken;

// 移除重复请求
const removePending = (config: AxiosRequestConfig) => {
  for (const key in pending) {
    const item: number = +key;
    const list: PendingType = pending[key];
    // 当前请求在数组中存在时执行函数体
    if (
      list.url === config.url &&
      list.method === config.method &&
      JSON.stringify(list.params) === JSON.stringify(config.params) &&
      JSON.stringify(list.data) === JSON.stringify(config.data)
    ) {
      // 执行取消操作
      // ElMessage.error("操作太频繁");
      // 从数组中移除记录
      pending.splice(item, 1);
    }
  }
};

/* 实例化请求配置 */
const instance = axios.create({
  // headers: {
  // token: tokenStore().returnToken,
  // },
  // 请求时长
  timeout: 1000 * 3000,
  // 请求的base地址 TODO:这块以后根据不同的模块调不同的api
  // baseURL: process.env.VUE_APP_API_URL,
  //     ? "测试"
  //     : "正式",
  // 表示跨域请求时是否需要使用凭证
  withCredentials: false,
});

instance.interceptors.request.use(
  (config) => {
    removePending(config);
    config.cancelToken = new CancelToken((c) => {
      pending.push({
        url: config.url,
        // method: config.method,
        params: config.params,
        data: config.data,
        cancel: c,
      });
    });
    if (!config?.headers) {
      throw new Error(
        `Expected 'config' and 'config.headers' not to be undefined`
      );
    }
    // tokenStore().changeToken(localStorage.getItem("access_token") ?? "");
    // config.headers["Authorization"] = "Bearer " + tokenStore().returnToken;
    // 登录流程控制中，根据本地是否存在token判断用户的登录情况
    // 但是即使token存在，也有可能token是过期的，所以在每次的请求头中携带token
    // 后台根据携带的token判断用户的登录情况，并返回给我们对应的状态码
    // 而后我们可以在响应拦截器中，根据状态码进行一些统一的操作。
    // const token = store.state.token;
    // localStorage.setItem('token', token);
    return config;
  },
  (error) => {
    ElMessage.error(error.data.error.message);
    return Promise.reject(error.data.error.message);
  }
);

// 响应拦截器
instance.interceptors.response.use(
  function (config) {
    // dataList.show = true
    removePending(config.config);
    // 请求成功
    if (config.status === 200 || config.status === 204) {
      // setTimeout(() => {
      //   // dataList.show = false
      // }, 400)
      return Promise.resolve(config);
    } else {
      return Promise.reject(config);
    }
    // 请求失败
  },
  function (error) {
    const { response } = error;
    if (response) {
      // errorHandle(response.status, response.data.message);
      // 超时重新请求
      const config = error.config;
      // 全局的请求次数,请求的间隙
      const [RETRY_COUNT, RETRY_DELAY] = [0, 1000];

      if (config && RETRY_COUNT) {
        // 设置用于跟踪重试计数的变量
        config.__retryCount = config.__retryCount || 0;
        // 检查是否已经把重试的总数用完
        if (config.__retryCount >= RETRY_COUNT) {
          errorHandle(response.status, response.headers["www-authenticate"]);
          return Promise.reject(response || { message: error.message });
        }
        // 增加重试计数
        config.__retryCount++;
        // 创造新的Promise来处理指数后退
        const backoff = new Promise<void>((resolve) => {
          setTimeout(() => {
            resolve();
          }, RETRY_DELAY || 1);
        });
        // instance重试请求的Promise
        return backoff.then(() => {
          return instance(config);
        });
      }

      return Promise.reject(response);
    } else {
      // 处理断网的情况
      // eg:请求超时或断网时，更新state的network状态
      // network状态在app.vue中控制着一个全局的断网提示组件的显示隐藏
      // 后续增加断网情况下做的一些操作
      // store.commit('networkState', false);
    }
  }
);

// 只需要考虑单一职责，这块只封装axios
export default instance;
