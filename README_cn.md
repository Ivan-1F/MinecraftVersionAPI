Minecraft Version API
-----

一个用于获取 Minecraft 服务端版本的 MCDReforged API 插件

包含一个简单的版本格式化器来将 Minecraft 版本格式化为类语义化版本（灵感来自 Fabric Loader） 

成功格式化后的版本可以被 MCDR 的 `Version` 类解析

**警告**: 此插件仅在常见版本原版服务端测试，如果发现任何与其他服务端核心的兼容性问题，请[发起一个 issue](https://github.com/Ivan-1F/MinecraftVersionAPI/issues/new)

## 它是如何工作的？

此插件会解析来自类似下面的服务器标准输出：

```
[Server thread/INFO]: Starting minecraft server version 1.15.2
```

然后插件就能拿到版本了

## 使用

导入 MinecraftVersionAPI：

```python
import minecraft_version_api
```

你可以在插件元数据中声明对本 API 的依赖：

```json
{
    "dependencies": {
        "minecraft_version_api": "*",
    }
}
```

### API

```python
def get_minecraft_version() -> Optional[Tuple[str, str]]
```

获取 Minecraft 服务器的版本

返回一个包含原始版本名和格式化后版本的元组。如果插件无法获取版本，返回 None

示例：`('22w13a', '1.19-snapshot.22.13.a')`
