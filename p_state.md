Linux可以使用cpufreq工具来调节CPU的P-STATE等级。具体步骤如下：

1. 首先，需要查看可用的CPU频率：

```
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_available_frequencies
```

这会输出可用的CPU频率列表，例如：

```
2000000 1800000 1600000 1400000 1200000 1000000 
```

2. 接下来，需要查看当前的CPU频率：

```
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq
```

这会输出当前CPU的工作频率，例如：

```
2000000
```

3. 调整CPU的P-STATE等级：

使用以下命令将CPU频率设置为指定的频率（例如1600000）：

```
sudo cpufreq-set -f 1600000
```

也可以使用以下命令将CPU频率设置为可用频率列表中的最小值：

```
sudo cpufreq-set -f $(cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_available_frequencies | awk '{print $NF}')
```

4. 恢复默认设置：

使用以下命令将CPU频率设为默认值：

```
sudo cpufreq-set -r
```

这会恢复到系统默认的CPU频率设置。

注意：需要使用root权限来运行这些命令。另外，这些命令的具体参数和用法可能因不同的Linux发行版和CPU型号而有所不同，请参考相关的文档和手册。