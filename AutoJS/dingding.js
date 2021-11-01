// Auto.js文档： https://hyb1996.github.io/AutoJs-Docs/#/?id=综述

function checkTime() {
    var curr_time = new Date();
    var now_Hours = curr_time.getHours();
    var now_Minutes = curr_time.getMinutes();
    var now_day = curr_time.getDay();

    if (now_day < 6) {
        var ran_minute = Math.round(Math.random() * 10);
        if (now_Hours == 8 && now_Minutes == ran_minute) {
            log("打卡时间 -> " + now_Hours + ':' + (ran_minute.toString().length == 1?'0' + ran_minute.toString():ran_minute.toString()));
        }
        else if (now_Hours == 21 && now_Minutes == ran_minute)  {
            log("打卡时间 -> " + now_Hours + ':' + (ran_minute.toString().length == 1?'0' + ran_minute.toString():ran_minute.toString()));
        } else {
            log("睡眠5分钟，再次调用");
            sleep(1000 * 60 * 5);
            checkTime();
        }
    }
}

function keepDrow(){
    device.wakeUpIfNeeded();
    device.keepScreenOn();
    log("尝试唤醒");
    if(!device.isScreenOn()){
        log("未唤醒");
        device.wakeUpIfNeeded();
        keepDrow();
    }
}

// 判断是否未登录 未登录则登陆
function doLogin(phone, password){
    // id() 获取控件的id，如果一个控件没有id，则返回null。
    /* findOne(): 根据当前的选择器所确定的筛选条件，对屏幕上的控件进行搜索，直到屏幕上出现满足条件的一个控件为止，并返回该控件。
                  如果找不到控件，当屏幕内容发生变化时会重新寻找，直至找到。需要注意的是，如果屏幕上一直没有出现所描述的控件，则该函数会阻塞，直至所描述的控件出现为止。因此此函数不会返回null。
    */
    // findOnce(): 根据当前的选择器所确定的筛选条件，对屏幕上的控件进行搜索，如果找到符合条件的控件则返回该控件；否则返回null。
    // findOnce() 为什么找不到控件？
    // var phone = id('et_phone_input').findOnce();  // 手机号
    // var password = id('et_pwd_login').findOnce();  // 密码
    if (id("et_pwd_login").exists()) { //判定是否在登录页面
        var but_phone = id('et_phone_input').findOne();
        var but_password = id('et_pwd_login').findOne();
        but_phone.setText(phone);
        but_password.setText(password);

        sleep(1000);
        id('cb_privacy').findOne().click();  // 勾选服务协议
        id("btn_next").findOne().click();  // 点击登录按钮
    } else {
        if (className("android.widget.RelativeLayout").exists()) {
            log("账号已登录")
            sleep(500);
        } else {
            log("未检测到钉钉活动页面 -> 重启钉钉")
            doLogin();
        }
    }
}

function daka() {
    /* 下面的方法不行，为什么？
    id('home_app_item').findOne().click();
    id('home_bottom_tab_icon').findOne().click();
    id('home_bottom_tab_icon_group').findOne().click();

    textMatches(/(.*工作台.*)/).findOne().click();
    descMatches(/(.*工作台.*)/).findOne().click();
    */

    // bounds(left, top, right, buttom) 一个控件的bounds属性为这个控件在屏幕上显示的范围。我们可以用这个范围来定位这个控件。尽管用这个方法定位控件对于静态页面十分准确，却无法兼容不同分辨率的设备；同时对于列表页面等动态页面无法达到效果，因此使用不推荐该选择器。
    sleep(1000);
    bounds(432, 1735, 648, 1893).click();  // 工作台
    sleep(3000);
    bounds(69, 1077, 186, 1197).click();  // 考勤打卡
    sleep(3000);
    bounds(342, 891, 738, 1284).click();  // 打卡按钮
}

function main () {
    checkTime();  // 检查当前时间是否在打卡时间范围内

    device.wakeUpIfNeeded();  // 如果屏幕没有点亮，则唤醒设备。
    auto.waitFor('fast');  // 检查无障碍服务是否已经启用，如果没有启用则跳转到无障碍服务启用界面，并等待无障碍服务启动；当无障碍服务启动后脚本会继续运行。因为该函数是阻塞的，因此除非是有协程特性，否则不能在ui模式下运行该函数，建议在ui模式下使用auto()函数。
    keepDrow();

    home();  // 模拟按下Home键。返回是否执行成功。 此函数依赖于无障碍服务。
    sleep(500);

    launchApp('钉钉');
    sleep(5000);
    // launch('com.alibaba.android.rimet');  // 打开钉钉

    doLogin('账号', '密码');  // 登录

    daka();  // 打卡

    device.cancelKeepingAwake();  // 取消设备保持唤醒状态。用于取消device.keepScreenOn(), device.keepScreenDim()等函数设置的屏幕常亮。
}

main();
