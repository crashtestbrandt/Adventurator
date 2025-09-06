## Contributing to Adventurator

Welcome! 🎲

This guide will walk you through how to safely collaborate on this repository using Git and GitHub.

---

1. Getting Started
  1.	Install Git
    * Download Git if you don’t already have it.
    * On macOS/Linux, you can also use Homebrew or your package manager.
	2. Clone the repository

	    ```
        git clone https://github.com/crashtestbrandt/Adventurator.git
        cd Adventurator
	    ```

	3. Set your Git identity (only once on your machine):
	
	    ```
        git config --global user.name "Your Name"
        git config --global user.email "you@example.com"
        ```

2. Branching Workflow

    We use a feature-branch workflow:
	 
    * main → always stable, deployable
    * Work happens on branches (feature/..., bugfix/..., docs/...)

      Create a new branch

	  ```
      git checkout main
      git pull origin main   # make sure you’re up to date
      git checkout -b feature/short-description
      ```

      Examples:

      * feature/add-sheet-crud
      * bugfix/fix-dice-parser
      * docs/update-readme

3. Making Changes
	1.	Edit files in src/Adventurator/ or other folders.
	2.	Check your changes locally:
	
	   * Run the tests:

	     ```
         make test
	     ```

       * Run the linter:

         ```
         make lint
         ```

       * Start the app locally:
  
         ```
	     make run
	     ```

    3. Stage and commit
 

	    ```
        git add <files>
        git commit -m "Short, clear message about what you did"
	    ```

        Tip: Keep commits small and focused. Use present tense, e.g., "add transcript model".

4. Keeping Your Branch Updated

    While working, keep your branch synced with main:

    ```
    git fetch origin
    git checkout main
    git pull origin main
    git checkout feature/your-branch
    git merge main
    ```

    If there are conflicts, Git will mark them--fix manually, then:

    ```
    git add <fixed files>
    git commit
    ```

5. Pushing & Pull Requests (PRs)
	1. Push your branch
	
        ```
        git push -u origin feature/your-branch
	    ```


	2. Open a Pull Request
      * Go to the repo on GitHub
      * Click "Compare & pull request"
      * Fill in the template:
        * What problem you solved
        * What changes you made
        * How to test it
	3. Get a review
      * Another team member reviews and approves.
      * Make changes if requested, then push again:
		
         ```
         git add <files>
         git commit -m "address review comments"
         git push
	     ```
			
	4. Merge
	   * Once approved and checks pass, Squash & Merge into main.

6. Best Practices

    * One branch = one task. Don’t mix unrelated changes.
    * Write meaningful commit messages.
    * Run tests and lint before pushing.
    * Never commit secrets (API keys, passwords, tokens).
    * Ask questions early--better to clarify than guess.

7. Common Commands Cheat Sheet

| Task | Command|
|------|--------|
| Clone repo | `git clone <url>` |
| New branch | `git checkout -b feature/thing` |
| Switch branch | `git checkout branch-name` |
| See status |	`git status` |
| Stage file	| `git add file.py` |
| Commit staged changes | `git commit -m "message"` |
| Pull latest main |	`git pull origin main` |
| Merge main into branch |	`git merge main` |
| Push branch to GitHub	| `git push -u origin feature/thing` |
| View log (recent commits) | `git log --oneline --graph --decorate` |

8. Troubleshooting
   * "I accidentally committed to main"
     * Make a branch from main, reset main:

        ```
        git checkout -b feature/fix-branch
        git push -u origin feature/fix-branch
	    ```

        Then restore main with:

	    ```
        git checkout main
        git reset --hard origin/main
	    ```
	   
   * Merge conflicts
      * Open the conflicted file, look for <<<<<<< and >>>>>>>, fix manually, then:

	    ```
        git add file.py
        git commit
	    ```

   * Forgot to pull before pushing
      * Run:

	     ```
        git pull --rebase origin main
        git push
	    ```

9. Where to Ask for Help
   * Post questions in the team’s chat channel
   * Tag @repo-maintainers in your PR if you need review
   * For Git basics: GitHub Docs
