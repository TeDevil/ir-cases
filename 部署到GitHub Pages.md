# 部署到 GitHub Pages

> 目标：拿到一个 `https://<用户名>.github.io/ir-cases/` 的网址，
> 手机打开后「添加到主屏幕」，得到一个**全屏、断网也能用**的图标。
>
> 全程约 10 分钟。第一页部署后要等 1–3 分钟生效。

---

## 开始之前，先知道四件事

| 事项 | 说明 |
|---|---|
| **免费版只能公开仓库** | GitHub 免费账户的 Pages 只对 **Public** 仓库生效。仓库公开 = **程序代码公开**，但里面没有任何病例数据。 |
| **网址谁都能打开** | 所以 App 里**只放程序，不放数据**。你录的每一条都只存在自己手机的浏览器里。 |
| **GitHub 是 https** | 这一点最关键：只有 https 才允许注册 Service Worker，才有「断网也能打开」。这也正是它比局域网 http 强的地方。 |
| **数据出口是"导出文件"** | GitHub Pages（https）不能直接连到家里的病例库（http 局域网）—— 浏览器会按「混合内容」拦掉。所以流程是：手机导出 → 电脑导入。 |

> 本仓库和你的 CBCT 记录 App（`TeDevil/IR`）是同一套路子，但**要单独建一个仓库**，
> 不要往 `IR` 里混，否则两个 app 的 Service Worker 会互相抢缓存。

---

## 第 0 步：先在电脑上试一下（可选，2 分钟）

在 `介入病例库\mobile_pwa\` 目录下打开 PowerShell：

```powershell
..\.venv\Scripts\python.exe serve.py
```

它会打印一个 `http://192.168.x.x:8000/index.html` 地址。
手机连同一个 WiFi 打开，就能先看看界面、试着录两条。

> 这一步下「离线缓存」会显示**未启用**，是正常的（http 下不允许）。
> 部署到 GitHub 之后就会变成**已启用**。

---

## 第 1 步：确认文件齐了

`mobile_pwa\` 里应该是这样（`_template.html` 不用传，那是构建用的）：

```
index.html                  ← 必须直接在仓库根目录
manifest.webmanifest
sw.js
.nojekyll
icons/
├── icon-180.png
├── icon-192.png
├── icon-512.png
└── icon-maskable-512.png
```

如果你改过 `caseapp\cases\choices.py`（比如加了新术式），
**先重新构建**再上传，否则手机上的下拉选项还是旧的：

```powershell
..\.venv\Scripts\python.exe ..\scripts\build_mobile_pwa.py
```

这个脚本会顺带把 `sw.js` 的缓存版本号改成新内容的哈希 ——
**你不需要手动改版本号**，这是和 CBCT 那个 app 不一样的地方。

---

## 第 2 步：新建仓库

1. 打开 <https://github.com> ，右上角 **+** → **New repository**
2. 填写：

   | 字段 | 填什么 |
   |---|---|
   | Repository name | `ir-cases`（**全小写，不要中文**） |
   | 公开性 | **Public** |
   | Add a README file | **不勾**（勾了会占掉首页，容易搞混） |
   | .gitignore / license | 都不选 |

3. **Create repository**

---

## 第 3 步：上传文件 ⚠️ 这一步最容易错

**关键：`index.html` 必须直接躺在仓库根目录。**

如果变成 `仓库/mobile_pwa/index.html`，网站根目录就没有 `index.html`，打开是 404。

操作：

1. 仓库页面点 **Add file** → **Upload files**
2. 在电脑上打开 `mobile_pwa` 文件夹
3. **进到文件夹里面**，`Ctrl+A` 全选**里面的内容**（不是选文件夹本身）
4. 拖进网页的上传框

   > `icons` 文件夹整个拖进去，GitHub 会保留目录结构。
   > `.nojekyll` 是隐藏文件，如果没被选中，需要单独建：
   > **Add file → Create new file**，名字填 `.nojekyll`，内容留空，提交。

5. 拉到底部 **Commit changes**

### 上传后必须核对

回到仓库首页，文件列表**第一层就应该看到 `index.html`**。
如果看到的是 `mobile_pwa` 这样的文件夹，说明套了一层，要重来。

---

## 第 4 步：开启 Pages

1. 仓库上方 **Settings**
2. 左侧栏往下找 **Pages**
3. **Source** = **Deploy from a branch**
4. **Branch** = `main`，文件夹 = **/ (root)**
5. **Save**
6. 等 1–3 分钟刷新，顶部出现绿色提示：

   ```
   Your site is live at https://<用户名>.github.io/ir-cases/
   ```

7. 同一页面向下，确认 **Enforce HTTPS** 已勾上

---

## 第 5 步：手机上装成 App

**必须用 Safari（iPhone）或 Chrome（安卓）**，不要用微信内置浏览器。

1. 浏览器打开 `https://<用户名>.github.io/ir-cases/`
2. 页面顶部右上角应该显示 **「离线可用」**
   - 显示「需 https」→ 地址不是 https
   - 显示「缓存失败」→ 多半是 `sw.js` 没上传成功
3. 点 **分享** → **添加到主屏幕**
4. 名字会自动填「介入病例库」，点 **添加**

以后从桌面图标进，不要再用浏览器开。

---

## 第 6 步：验证真的能离线

1. 手机开**飞行模式**
2. 从桌面图标打开
3. 能正常打开、能录一条 → 成功

---

## 第 7 步：录完之后怎么回到病例库

```
手机 app → 「导出」→「导出 JSON 文件」
    ↓ 发到电脑（微信文件传输 / USB / 邮件，都行）
电脑 → 病例库 → /m/bulk/ →「方式一：选手机导出的文件」
    ↓ 解析预览 → 确认创建
病例入库，之后补影像、分期、随访
```

> 为什么不用「点一下同步」：GitHub Pages 是 https，家里的病例库是 http 局域网，
> 浏览器会直接拦掉这种请求（混合内容）。
> 而且 localStorage 按来源隔离 —— 两个地址存的数据互相看不见。
> 所以「导出文件 → 导入」是唯一可靠的路径，不是偷懒。

---

## 以后怎么更新

### 改了什么之后

1. 改 `mobile_pwa/_template.html`（或 `choices.py`）
2. 跑构建：
   ```powershell
   ..\.venv\Scripts\python.exe ..\scripts\build_mobile_pwa.py
   ```
3. 把 `index.html` 和 `sw.js` 一起上传（GitHub 网页 **Add file → Upload files**，同名覆盖）
4. **手机上：删掉桌面图标 → 浏览器重新打开 → 重新「添加到主屏幕」**

> 为什么还要重装：Service Worker 会保留上一版。
> 虽然缓存版本号是自动变的，但 iOS 有时不会主动更新已安装的图标。

### 别忘了

改 `choices.py` 加了新术式/新病种之后，**必须重新构建并上传**，
否则手机上的下拉框还是旧的 —— 而电脑端已经是新的，两边就对不上了。

---

## 常见问题

**Q：打开是 404**
A：`index.html` 不在仓库根目录。看仓库首页第一层有没有它。

**Q：显示的是 README**
A：建仓库时勾了 "Add a README"，而 `index.html` 没传上去。

**Q：显示「需 https」**
A：地址是 http，或者用了 IP 访问。GitHub Pages 强制 https，检查是不是打成了 `http://`。

**Q：Safari 里找不到「添加到主屏幕」**
A：① 无痕模式 → 退出；② 页面没加载完；③ 用的是微信内置浏览器。

**Q：图标是灰的/是张网页截图**
A：iOS 缓存了旧的 `apple-touch-icon`。删掉图标，清一下该站点数据，重新添加。

**Q：Actions 里那条任务红了**
A：点进去看日志。绝大多数是**文件路径大小写**不一致（`icons/` vs `Icons/`）——
GitHub Pages 区分大小写。

**Q：能不能设成私密，只有我们科能看**
A：GitHub Pages 没有访问控制。要限制访问得换 Cloudflare Access 之类，或者放内网。
但记住：**App 里没有数据，只有程序**，公开的风险很低。

**Q：能不能把病例数据也放上去**
A：**不能，也绝对不要。** 仓库是公开的，任何人（包括搜索引擎）都能抓取。

**Q：手机丢了怎么办**
A：记录在手机浏览器里，随浏览器数据一起消失。
所以：**定期导出 JSON 备份**（设置页有「导出备份」）。
另外建议开启手机锁屏密码；数据本身不含身份信息，但仍有反推风险。

**Q：换手机了**
A：新手机装好 app 后，用「从备份恢复」导入旧手机导出的 JSON。
注意：**必须先导出再换**，否则记录跟着旧手机走了。

---

## 一次性核对清单

上传前：

- [ ] 改过 `choices.py` 的话已经重新构建过
- [ ] `index.html`、`sw.js`、`manifest.webmanifest`、`.nojekyll`、`icons/` 齐了
- [ ] `index.html` 和 `icons` 在同一层

上传后：

- [ ] 仓库首页第一层能看到 `index.html`
- [ ] Settings → Pages 已开，Source = main / (root)
- [ ] 绿色提示里有网址
- [ ] 浏览器打开正常

手机：

- [ ] 用 Safari / Chrome 打开（不是微信）
- [ ] 右上角显示 **「离线可用」**
- [ ] 分享 → 添加到主屏幕
- [ ] 飞行模式下从图标打开正常
- [ ] 录一条 → 导出 JSON → 电脑端能导入成功

---

## 附：命令行版（熟悉 git 的话更快）

```bash
git clone https://github.com/<用户名>/ir-cases.git
# 把 mobile_pwa 里的文件复制进去（index.html 与 icons 同级，去掉 _template.html）
cd ir-cases
git add .
git commit -m "更新手机建档"
git push origin main
```

推上去 1–2 分钟自动生效。
