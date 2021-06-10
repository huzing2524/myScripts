auto();
var appName=rawInput("请输入app的名称");
launchApp(appName);
sleep(1000);
setScreenMetrics(1080, 1920);

sleep(1000);

function getRandom (n, m) {
    var num = Math.floor(Math.random() * (m - n + 1) + n)
    return num
}

var num = 200;
while(num > 1){
    swipe(device.width / 2, 1300, device.width / 2, 300, 2000);
    sleep(getRandom(5, 15) * 1000);  // 视频观看时间：5~15秒
}
