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



    apt-get install cpufrequtils
    要设置CPU频率，您可以使用以下命令格式：
    ```
    sudo cpufreq-set -c <CPU编号> -u <最大频率> -d <最小频率> -g <性能模式>
    
    sudo cpufreq-set -c 0 -g performance
    ```

    其中，-c参数用于指定CPU编号，如果您的系统只有一个CPU，可以忽略此参数；-f参数用于指定最大频率，单位是千赫兹；-u参数用于指定最小频率；-g参数用于指定性能模式，您可以选择以下其中一个：

    - performance：最高性能模式
    - powersave：最低功耗模式
    - ondemand：根据使用情况动态调整频率
    - conservative：类似于ondemand，但尽可能在较低频率下运行以节省更多功耗

    例如，如果您要将CPU最大频率设置为2.5 GHz，最小频率设置为1 GHz，性能模式设置为powersave，可以使用以下命令：

    ```
    sudo cpufreq-set -f 2500000 -u 1000000 -g powersave
    ```

    需要注意的是，这只是临时设置，重启系统后会失效。如果您想让设置永久生效，需要编辑CPU频率配置文件，在其中添加类似上面命令的配置。