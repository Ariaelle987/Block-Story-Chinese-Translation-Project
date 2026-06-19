# Block Story Chinese Translation Project / Block Story 中文翻译项目

[简体分支](https://github.com/Ariaelle987/Block-Story-Chinese-Translation-Project/tree/simplified-chinese)  
[繁体分支](https://github.com/Ariaelle987/Block-Story-Chinese-Translation-Project/tree/traditional-chinese)

---

## About / 关于

This project provides Chinese localization for *Block Story*. Simplified Chinese is maintained in the `simplified-chinese` branch, while Traditional Chinese (Taiwan) is automatically generated via GitHub Actions.  
本项目为 *Block Story* 提供中文翻译。简体中文在 `simplified-chinese` 分支维护，繁体中文（台湾）通过 GitHub Actions 自动生成。

---

## Downloads / 下载

| Version | Branch | Download |
|----------|--------|----------|
| Simplified Chinese | `simplified-chinese` | [ZIP](https://github.com/Ariaelle987/Block-Story-Chinese-Translation-Project/archive/refs/heads/simplified-chinese.zip) |
| Traditional Chinese (Taiwan) | `traditional-chinese` | [ZIP](https://github.com/Ariaelle987/Block-Story-Chinese-Translation-Project/archive/refs/heads/traditional-chinese.zip) |

繁体版本由简体版本自动同步生成。

---

## Workflow / 工作机制

When `.txt` files in `simplified-chinese` are updated, a GitHub Actions workflow automatically:  
当 `simplified-chinese` 分支 `.txt` 文件更新后，GitHub Actions 会自动：

- Converts Simplified Chinese → Traditional Chinese (OpenCC s2tw)  
  使用 OpenCC（s2tw）进行简繁转换  
- Applies Taiwan-specific terminology corrections  
  应用台湾用语词典修正  
- Commits results to `traditional-chinese` branch  
  提交到 `traditional-chinese` 分支  

---

## Contributing / 贡献方式

Edit `.txt` files in `simplified-chinese` branch and push changes. Traditional Chinese will update automatically.  
直接修改 `simplified-chinese` 分支 `.txt` 文件并提交即可，繁体版本自动更新。

---

## Notes / 注意事项

Do NOT edit files in `traditional-chinese` branch. All changes must be made in `simplified-chinese`. Manual edits will be overwritten.  
请勿直接修改 `traditional-chinese` 分支，否则会被自动流程覆盖，所有修改应在 `simplified-chinese` 进行。

---

## License / 许可

This project provides localization resources for *Block Story*.  
Original game content and assets belong to Big Cube Interactive, LLC.

This repository is intended as a contribution to the official localization workflow and may be reviewed or adopted by the development team.

本项目为 *Block Story* 提供本地化翻译资源。  
原始游戏内容及资产版权归 Big Cube Interactive, LLC 所有。

本仓库用于向官方本地化流程提供翻译资源，开发团队可能审核或采纳其中内容。

---

## Credits / 致谢

- Ariaelle987 — Maintainer / 维护者  
- icefox619 — Contributor / 贡献者  
- jjyzsl2010722-ui — Contributor / 贡献者  
- OpenCC — Simplified-Traditional conversion tool / 简繁转换工具  

---

## Contact / 联系

Open an Issue for feedback or questions.  
如有问题或建议，请提交 Issue。
