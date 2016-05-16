# Puppet Laguage Style Guide
Puppet Language Style Guide: Version 2.0.1
Puppet: Version 3.7+

## 1. 术语

本文中"MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", 和 "OPTIONAL" 这些术语均可按照 [RFC 2119](http://www.faqs.org/rfcs/rfc2119.html) 中的定义来解释。（本文对应为 「必须」，「一定不」，「需要」，「需要」，「不要」，「应该」，「不应该」，「建议」，「可以」，「可选」）

除非特别声明，本文所有的讨论均围绕 Puppet（如 Puppet 模块, Puppet 类等）进行。为了简便，'Puppet' 会被省略。

## 2. 目的

本风格指南的目的是为了提升模块（Puppet Labs或社区的模块）格式的一致性，能够给 Puppet 模块开发者一个通用的模式，设计和风格进行参考。另外，一致的代码风格和模块结构也会让持续的开发更加轻松。

## 3. 指导方针

我们不可能覆盖到你在开发 Puppet 代码或者模块时的种种情形。最后，你可能需要自己来做出决定。当你需要做决定时，记住下面这几点通用准则：

1. **保持可读性**

如果你需要在两个同样效果的方案之间进行抉择，那么选择更具可读性的方案。可读性是一个主观的概念，如果你能够轻松理解三个月前写的代码，这就是一个好的开始。对代码修改后的 diff 输出的可读性是需要首要考虑的因素。

2. **简洁有度是关键**

有疑问时，选择更简洁的答案。一个模块应该只包含用于完成目标的相关资源。如果你发现当你试图描述你的模块的功能时，需要使用「和」字，那么就该考虑从「和」开始拆分你的模块了。你应该只有一个目标，所有的类和参数都是为了实现这一个目标。

3. **把模块当做软件对待**

至少，你应该这样看待你的模块。当需要做决定时，选择那个更易于长期维护的。

## 4. 版本控制

你的模块应该进行版本控制。我们建议（并且也在使用）[语义化版本](http://semver.org/lang/zh-CN/) 的方式，即使用 x.y.z 的方式。主版本号的增加表示不兼容的 API 修改，次版本号的增加表示向下兼容的功能性新增，修订号的增加表示向下兼容的 bug fix.

## 5. 空格，缩进和空白

模块的 manifest：

- 必须使用两个空格的缩进
- 一定不要使用默认宽度的文字制表符
- 一定不要在行尾包含空白
- 必须在所有的资源属性和参数定义后加上逗号
- 一行的宽度不应该超过 140 个字符
- 多行属性的定义中的 `=>` 符号应该对齐，使用哈希字典时要将其排布的更具可读性

## 6. 引号

- 所有的字符串都应该使用单引号，除非包含变量或者单引号本身
- 如果字符串是一个有限的选项（例如 `present/absent`），引号不是必须的
- 在字符串中的所有变量替换都应该使用大括号。例如：

规范示例：

```
    "/etc/${file}.conf"
    "${::operatingsystem} is not supported by ${module_name}"
```

不规范示例：

```
    "/etc/$file.conf"
    "$::operatingsystem is not supported by $module_name"
```

- 表示本意的变量不应该使用引号，除非被用作资源标题（resource title）。例如：

规范示例：

```
    mode => $my_mode
```

不规范示例：

```
    mode => "$my_mode"
    mode => "${my_mode}"
```

- 如果一个字符串包含单引号本身，此时应该使用双引号而不是去进行转义。

规范示例：

```
warning("Class['apache'] parameter purge_vdir is deprecated in favor of purge_configs")
```

不规范示例：

```
warning('Class[\'apache\'] parameter purge_vdir is deprecated in favor of purge_configs')
```

## 7. 注释

你应该使用 `#` 格式的注释（`# This is a comment`）。注释要解释的 **why**，而不是 **how**.

规范示例：

```
# Configures NTP
file { '/etc/ntp.conf': … }
```

不规范示例：

```
/* Creates file /etc/ntp.conf */
file { '/etc/ntp.conf': … }
```

## 8. 模块的元信息（metadata）

每一个公开可用的模块必须在 `metadata.json` 文件中定义元信息。你的元信息应该遵循下面的格式：

```
    {
      "name": "examplecorp-mymodule",
      "version": "0.1.0",
      "author": "Pat",
      "license": "Apache-2.0",
      "summary": "A module for a thing",
      "source": "https://github.com/examplecorp/examplecorp-mymodule",
      "project_page": "https://github.com/examplecorp/examplecorp-mymodule",
      "issues_url": "https://github.com/examplecorp/examplecorp-mymodules/issues",
      "tags": ["things", "stuff"],
      "operatingsystem_support": [
        {
          "operatingsystem":"RedHat",
          "operatingsystemrelease": [
            "5.0",
            "6.0"
          ]
        },
        {
          "operatingsystem": "Ubuntu",
          "operatingsystemrelease": [ 
            "12.04",
            "10.04"
         ]
        }
      ],
      "dependencies": [
        { "name": "puppetlabs/stdlib", "version_requirement": ">= 3.2.0 <5.0.0" },
        { "name": "puppetlabs/firewall", "version_requirement": ">= 0.4.0 <5.0.0" },
      ]
    }
```

更完整的 `metadata.json` 文件格式的文档在[这里](http://docs.puppetlabs.com/puppet/latest/reference/modules_publishing.html?_ga=1.122362123.1293671910.1443759419#write-a-metadatajson-file)

### 8.1. 依赖

你的模块的硬性依赖必须在模块的 `metadata.json` 文件中定义清楚。非硬性依赖应该在 `README.md` 文件中声明，并且一定不要写在 `metadata.json` 文件中而被当做硬需求。非硬性依赖指仅在某些特殊情况下所需要的依赖。（例如，可以参考[rabbitmq 模块](https://forge.puppetlabs.com/puppetlabs/rabbitmq?_ga=1.100728321.1293671910.1443759419#module-dependencies)）

不要无节制的定义硬性依赖。

## 9. 资源

### 9.1. 资源名

所有资源的标题（title）必须使用引号。如果你使用一个包含标题的数组，那么数组中的所有的标题都必须使用引号，不要对数组本身使用引号。

规范示例：

```
    package { 'openssh': ensure => present }
```

不规范示例：

```
    package { openssh: ensure => present }
```

### 9.2. 箭头的对齐

一个资源的属性列表中的所有的 `=>` 符号应该对齐。`=>` 应该和最长属性名之间一个空格的距离。嵌套的代码块必须使用两个空格缩进，并且嵌套代码中的 `=>` 也应该对齐（与最长属性名之间一个空格的距离）。

规范示例：

```
    exec { 'hambone':
      path => '/usr/bin',
      cwd  => '/tmp',
    }

    exec { 'test':
      subscribe   => File['/etc/test'],
      refreshonly => true,
    }

    myresource { 'test':
      ensure => present,
      myhash => {
        'myhash_key1' => 'value1',
        'key2'        => 'value2',
      },
    }
```

不规范示例：

```
    exec { 'hambone':
      path  => '/usr/bin',
      cwd => '/tmp',
    }

    exec { 'test':
      subscribe => File['/etc/test'],
      refreshonly => true,
    }
```

### 9.3. 属性顺序

如果一个资源定义中包含 `ensure` 属性，那么它应该第一个被定义，这样用户可以快速的查看一个资源是否被创建或删除。

规范示例：

```
    file { '/tmp/readme.txt':
      ensure => file,
      owner  => '0',
      group  => '0',
      mode   => '0644',
    }
```

### 9.4. 资源排列

在一个 manifest 文件中，资源应该按照彼此间的逻辑关系而不是资源类型来排列。不要在大括号中使用分号来定义多个资源。

规范示例：

```
    file { '/tmp/dir':
      ensure => directory,
    }

    file { '/tmp/dir/a':
      content => 'a',
    }

    file { '/tmp/dir2':
      ensure => directory,
    }

    file { '/tmp/dir2/b':
      content => 'b',
    }
```

不规范示例：

```
    file { '/tmp/dir':
      ensure => directory,
    }

    file { '/tmp/dir2':
      ensure => directory,
    }
    
    file { '/tmp/dir/a':
      content => 'a',
    }

    file { '/tmp/dir2/b':
      content => 'b',
    }
```

### 9.5. 软连接

软连接必须使用 `ensure => link` 的方式来定义，同时指定 `target` 属性。这种方式更能提示用户创建了一个软连接。

规范示例：

```
    file { '/var/log/syslog':
      ensure => link,
      target => '/var/log/messages',
    }
```

非规范示例：

```
    file { '/var/log/syslog':
      ensure => '/var/log/messages',
    }
```

### 9.6. 文件权限
- POSIX 数字标记形式必须使用 4 位数字。
- POSIX 符号标记形式必须是一个字符串。
- 你不应该对 Windows 文件使用文件权限，而应该使用 [acl module](https://forge.puppetlabs.com/puppetlabs/acl?_ga=1.56360619.1293671910.1443759419)。
- 应该尽可能的使用数字标记格式。

规范示例：

```
  file { '/var/log/syslog':
      ensure => file,
      mode   => 'o-rwx',
  }
```

非规范示例：

```
    file { '/var/log/syslog':
      ensure => present,
      mode   => 644,
    }
```

### 9.7. 资源默认属性（[Resource Default](https://docs.puppetlabs.com/puppet/latest/reference/lang_defaults.html)）

应该有节制的使用资源默认属性功能，并且应该仅在 manifest 文件的边界处进行定义。它们可以被定义在：

- site.pp 的顶级作用域中
- 一个一定不会被声明或被其他类继承或被其他模块定义的类中

这样做是因为资源默认属性会通过动态作用域传播，很可能产生不可预期的效果。

规范示例：

```
    # /etc/puppetlabs/puppet/manifests/site.pp:
    File {
      owner => 'root',
      group => '0',
      mode  => '0644',
    }
```

非规范示例：

```
    # /etc/puppetlabs/puppet/modules/apache/manifests/init.pp
    File {
      owner => 'nobody',
      group => 'nogroup',
      mode  => '0600',
    }

    concat { $config_file_path:
      notify  => Class['Apache::Service'],
      require => Package['httpd'],
    }
```

## 10. 类和定义

### 10.1. 文件分离

所有的类（class）和资源类型定义（define）都必须是模块的 `manifests` 目录下单独的文件。

规范示例：

```
    # /etc/puppetlabs/puppet/modules/apache/manifests

    # init.pp
      class apache { }
    # ssl.pp
      class apache::ssl { }
    # virtual_host.pp
      define apache::virtual_host () { }
 ```
 
把类和定义分离到单独的文件中和将它们全部定义在 `init.pp` 在功能上并没有区别，但是这样做能够使得模块的结构更加醒目，并且功能和结构更加清晰。

### 10.2. 类和定义内部的代码组织

类和定义必须被用来实现单个目标。下面是逐行的代码布局指南：

1. 第一行：类或者类型的名字。
2. 接下来若干行，如果需要：定义参数。
3. 接下来若干行：应该对参数进行校验，如果参数无效，则停止 catalog 的编译。
4. 接下来若干行，如果需要：应该声明本地变量并进行变量的相关操作。
5. 接下来若干行：声明资源。
6. 接下来：如果有必要的化，覆盖资源。

下面是遵循建议的风格的示例代码：

```
    # init.pp
    class myservice (
      $service_ensure     = $myservice::params::service_ensure,
      $package_list       = $myservice::params::package_list,
      $tempfile_contents  = $myservice::params::tempfile_contents,
    ) inherits myservice::params {

      if !($service_ensure in [ 'running', 'stopped' ]) {
        fail('ensure parameter must be running or stopped')
      }

      if !$package_list {
        fail("Module ${module_name} does not support ${::operatingsystem}")
      }

      # temp file contents cannot contain numbers
      case $tempfile_contents {
        /\d/: {
          $_tempfile_contents = regsubst($tempfile_contents, '\d', '', 'G')
        }
        default: {
          $_tempfile_contents = $tempfile_contents
        }
      }

      $variable = 'something'

      Package { ensure => present, }

      File {
        owner => '0',
        group => '0',
        mode  => '0644',
     }

      package { $package_list: }

      file { "/tmp/${variable}":
        ensure   => present,
        contents => $_tempfile_contents,
      }

      service { 'myservice':
        ensure    => $service_ensure,
        hasstatus => true,
      }

      Package[$package_list] -> Service['myservice']
    }

    # params.pp
    class myservice::params {
      $service_ensure = 'running'

      case $::operatingsystem {
        'centos': {
          $package_list = 'myservice-centos-package'
        }
        'solaris': {
          $package_list = [ 'myservice-solaris-package1', 'myservice-solaris-package2' ]
        }
        default: {
          $package_list = undef
        }
      }
    }
```

### 10.3. 公共的和私有的

我们建议你尽可能的将模块拆分为公共和私有的类和定义。公共的类和定义包含用来允许用户配置和自定义的部分，私有类是你不希望被用户通过参数修改的类。公共和私有的拆分方式可以让代码具有更好的重用性和可读性。

你应该通过在 README 中调用公共类来帮助用户区别公共类和私有类，确保所有的公共类都有完整的注释。

> 注意：从 stdlib 4.4.0 开始，引入了 `private` 函数来保护私有类，使其在模块外部调用时失败。可以使用这种方式来强制私有类不能被从模块外部调用。

### 10.4. 箭头链语法

尽可能使用[关系元参数（relationship metaparameter）](https://docs.puppetlabs.com/puppet/latest/reference/lang_relationships.html?_ga=1.96622495.1293671910.1443759419#relationship-metaparameters)而不是[链式箭头（chaining arrow）](https://docs.puppetlabs.com/puppet/latest/reference/lang_relationships.html?_ga=1.96622495.1293671910.1443759419#chaining-arrows)。当你有[大量的互相依赖或者顺序要求](https://github.com/puppetlabs/puppetlabs-mysql/blob/3.1.0/manifests/server.pp#L64-L72)时，可以使用链式语法。链式箭头必须使用从左至右方向的。

规范示例：

```
Package['httpd'] -> Service['httpd']
```

不规范示例：

```
Service['httpd'] <- Package['httpd']
```

### 10.5. 嵌套的类或定义

类和定义一定不能在其他类或者自定义资源中进行定义。类和定义应该尽可能的在节点作用域级别进行声明。如果一个类或定义中依赖其他的类或者定义，一定要在这些类或定义没有被定义时进行错误处理。

非常不规范：

```
    class apache {
      class ssl { ... }
    }
```

同样非常不规范：

```
    class apache {
      define config() { ... }
    }
```

### 10.6. 参数的显示顺序

在参数化的类和定义的声明中，必须参数应该在可选参数（例如有默认值的参数）之前列出。

规范示例：

```
class dhcp (
  $dnsdomain,
  $nameservers,
  $default_lease_time = 3600,
  $max_lease_time     = 86400
) {}
```

不规范示例：

```
    class ntp (
      $options   = "iburst",
      $servers,
      $multicast = false
    ) {}
```

### 10.7. 参数默认值

当编写一个接收参数的类时，应该为可选参数提供合适的默认值。合适的默认值可以让用户在声明类时不用显示的指定可选参数。参数的默认值应该在专门的参数类中定义，而不应该在类和定义中。

当定义参数默认值时：

- 当从模块的 param 类中调用变量时一定要使用完全限定名称空间格式的变量。这样可以避免变量的名称冲突。[Namespacing Variables](http://localhost:8000/guides/style_guide.html#namespacing-variables) 中有更多的相关文档。
- 对于用作维护作用的变量，应该使用 `_` 前缀来标识。

规范示例：

```
class my_module (
  $source = $my_module::params::source,
  $config = $my_module::params::config,
){}
```

不规范示例：

```
class my_module (
  $source = undef,
) {
  if $source {
    $_source = $source
  } else {
    $_source = $my_module::params::source
  }
}
```

### 10.8. 导出资源（Exported Resources）

导出资源应该尽量不要使用，除非一定需要。当使用导出资源时，在使用时，使用使用 `collect_exported` 参数来标明是否使用导出资源。

导出资源的收集应该使用[search expression](https://docs.puppetlabs.com/puppet/3.7/reference/lang_collectors.html?_ga=1.155898427.1293671910.1443759419#search-expressions)来进行选择，可以使用用户定义的 tag 参数来进行选择。

规范示例：

```
define haproxy::frontend (
  $ports            = undef,
  $ipaddress        = [$::ipaddress],
  $bind             = undef,
  $mode             = undef,
  $collect_exported = false,
  $options          = {
    'option'  => [
      'tcplog',
    ],
  },
) { … }
```

## 11. 类
### 11.1. 类继承
可以在一个模块内使用继承，一定不要跨模块名称空间使用继承。跨模块名称空间的依赖应该用其他方式来解决，例如 include 语句或者依赖关系定义。

规范示例：

```
    class ssh { ... }

    class ssh::client inherits ssh { ... }

    class ssh::server inherits ssh { ... }
```

不规范示例：

```
    class ssh inherits server { ... }

    class ssh::client inherits workstation { ... }

    class wordpress inherits apache { ... }
```

通常，如果可以使用别的方式替代，就不要使用继承。例如，如果想用继承的方式来覆盖类中关系定义，可以考虑使用一个类，并使用 `ensure` 参数和条件判断的关系声明。例如：

```
    class bluetooth (
      $ensure      = 'present',
      $autoupgrade = false,
    ) {
       # Validate class parameter inputs. (Fail early and fail hard)

       if ! ($ensure in [ 'present', 'absent' ]) {
         fail('bluetooth ensure parameter must be absent or present')
       }

       if ! ($autoupgrade in [ true, false ]) {
         fail('bluetooth autoupgrade parameter must be true or false')
       }

       # Set local variables based on the desired state

       if $ensure == 'present' {
         $service_enable = true
         $service_ensure = 'running'
         if $autoupgrade {
           $package_ensure = 'latest'
         } else {
           $package_ensure = 'present'
         }
       } else {
         $service_enable = false
         $service_ensure = 'stopped'
         $package_ensure = 'absent'
       }

       # Declare resources without any relationships in this section

       package { [ 'bluez-libs', 'bluez-utils']:
         ensure => $package_ensure,
       }

       service { 'hidd':
         enable         => $service_enable,
         ensure         => $service_ensure,
         status         => 'source /etc/init.d/functions; status hidd',
         hasstatus      => true,
         hasrestart     => true,
      }

      # Finally, declare relations based on desired behavior

      if $ensure == 'present' {
        Package['bluez-libs']  -> Package['bluez-utils']
        Package['bluez-libs']  ~> Service['hidd']
        Package['bluez-utils'] ~> Service['hidd']
      } else {
        Service['hidd']        -> Package['bluez-utils']
        Package['bluez-utils'] -> Package['bluez-libs']
      }
    }
```

记住：
类继承应该只为 `myclass::params` 形式的默认参数而使用。其他的情况都可以通过额外参数或判断逻辑来实现。

### 11.2. 关于公共模块的注意事项

当在一个公共模块中声明类时，应该使用 `include`, `contain` 或者 `require` 而不是资源形式的声明。这样可以避免类的重复生命。

## 12. 自定义资源（Defined Resource Types, Defines）

### 12.1. 唯一性

因为自定义资源可以有多个示例，资源的名字必须包含一个唯一的变量来避免重复声明。

规范示例：

```
define apache::listen {
  $listen_addr_port = $name

  # Template uses: $listen_addr_port
  concat::fragment { "Listen ${listen_addr_port}":
    ensure  => present,
    target  => $::apache::ports_file,
    content => template('apache/listen.erb'),
  }
}
```

不规范示例：

```
file { 'Required VHost directory':
  path   => '/etc/apache/vhost/corpsite',
  ensure => directory,
}
```

## 13. 变量

### 13.1. 变量名称空间

你必须为出了本地变量和继承变量外的所有变量指明名称空间。为了清晰性也可以指明继承变量的名称空间。不要隐藏继承的变量。

你应该在使用顶级域变量时（包括 facts）指明名称空间以避免作用域的问题。

规范示例：

```
    $::operatingsystem
```

不规范示例：

```
    $operatingsystem
```

### 13.2. 变量格式
当定义变量时，必须只能使用数字，小写字母和下划线。不要使用驼峰法（camelCasing），这会使得风格不同意。不要使用 `-`，这会导致语法问题。

规范示例：

```
$foo_bar
$some_long_variable
$foo_bar123
```

不规范示例：

```
$fooBar
$someLongVariable
$foo-bar123
```

## 14. 条件语句

### 14.1. 保持资源声明的简洁性

我们建议不要把资源声明和条件语句混合在一起。当在赋值时使用条件判断语句时，应该将判断逻辑代码和资源声明分离开。

规范示例：

```
    $file_mode = $::operatingsystem ? {
      'debian' => '0007',
      'redhat' => '0776',
       default => '0700',
    }

    file { '/tmp/readme.txt':
      ensure  => file,
      content => "Hello World\n",
      mode    => $file_mode,
    }
```

不规范示例：

```
    file { '/tmp/readme.txt':
      ensure  => file,
      content => "Hello World\n",
      mode    => $::operatingsystem ? {
        'debian' => '0777',
        'redhat' => '0776',
        default  => '0700',
      }
    }
```

### 14.2. Case 语句和 Selector

Case 语句必须有 default case。如果你想让 default case 什么也不做，也必须明确的包含一个 `default: {}`。

Case 和 selector 中的值必须使用引号。

Selector 应该只在你想让没有匹配值时中断 catalog 编译的情况下包含 default selection。

规范示例：

```
    case $::operatingsystem {
      'centos': {
        $version = '1.2.3'
      }
      'solaris': {
        $version = '3.2.1'
      }
      default: {
        fail("Module ${module_name} is not supported on ${::operatingsystem}")
      }
    }
```

当设置了 default case 时，如果无法预期结果，那么让没有匹配的 case 产生一个 failure。

## 15. Hiera

应该避免在公共模块中调用 Hiera 函数，因为不是所有的用户都有使用 Hiera。我们建议使用参数，它们能够被 Hiera 覆盖。

## 16. 示例

你的模块的 /examples 目录下应该包含对应的使用示例。

```
modulepath/apache/examples/{usecase}.pp
```

示例 manifest 文件应该清晰的示范如果声明类或自定义资源。示例 manifest 还应该将依赖的类声明，以确保可以使用 `puppet apply` 应用示例 manifest.

## 17. 模块文档

所有的公共模块都应该包含下面的文档

### 17.1. README

你的模块应该有一个 `.md` 或 `.markdown` 格式的 `README` 文件来说明如何使用。这里有一个 [Puppet Labs REAME 模板](https://docs.puppetlabs.com/puppet/latest/reference/READMEtemplate.txt?_ga=1.131339535.1293671910.1443759419)可以使用，也可以使用 `puppet module generate` 来生成包含 `README` 的模块。使用 `.md/.markdown` 格式的 `README` 可以确保它能够被 GitHub 和 Pupept Forge 渲染。

如果你的代码注释比较多，可以使用 Puppet 4 的 `puppet doc`. 如果使用 future parser，可以使用 [strings](https://github.com/puppetlabs/puppetlabs-strings) 替代 `puppet doc`。

这里有一个完整的关于写好 README 的[指南](https://docs.puppetlabs.com/puppet/latest/reference/modules_documentation.html?_ga=1.88219291.1293671910.1443759419)，总体来说，你需要

- 说明你的模块是做什么的
- 说明模块将可能修改用户系统的哪些部分（例如，“This module will overwrite everything in animportantfile.conf.”）
- 列出所有的类，自定义类型，provider 和参数，用户可能需要一个简短的描述，并知道参数的默认值是什么，有哪些可用选项。

### 17.2. CHANGELOG

你的模块应该包含一个 `.md/.markdown` 格式的 `CHANGELOG`。`CHANGELOG` 的内容：

- 每个版本都有对应的条目
- 列出每个版本中的功能和 bugfix
- 说明不向前兼容的变更

## 19. 检查代码风格

可以使用 [puppet-lint](http://puppet-lint.com/) 和 [metadata-json-lint](https://github.com/nibalizer/metadata-json-lint) 来检查代码风格。