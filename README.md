git 遠端 merge 遠端不同技巧

假如今天想將分支一的內容合併到分之二

1.
2. 先將 [分支一] pull 下來 `git pull origin [分支一]`
3. 切換到 [分之二] `git checkout [分支二]`
4. 將 [分支二] pull 下來 `git pull origin [分支二]`
5. 再將 [分支一] 的內容在 [分支二] 中 pull 下來 `git pull origin [分支一]`
6. 手動或自動 merge
7. 最後把 [分支二] push 上去就大功告成了 `git push origin [分支二]`
