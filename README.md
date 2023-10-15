# Pitchfork
A Python bot that uses OpenAI's GPT-4V to analyze the Dickinson College Caf Menus (Way to make something incredibly hard to parse) and utilizes SMTP + Jinja2 to email daily menus to a select list of people. The deployment of Pitchfork is done by setting a cronjob on a remote Linux VM to run every morning at 6:00 AM EST. 

If you want to be added to this list, please email chermsit@dickinson.edu or message WarpWing#3866 on Discord.

In addition, due to a lack of motivation, I've only included the basic dishes for the mainline. Outside of that, there are no updates for KOVE, Grains Bar, Grains Bar Sauce, Speciality Salad, Chef's Cold Plate or Deli Sandwich of the Day. If you're interested in helping to implement them, please feel free to submit a pull request or discuss them with me on GitHub Issues!

#To-Do List

- [x] Finalized Raw Data from GPT4V
- [ ] Keep data scheme consistent(Non Priority) (Eg. instead of Grill1, Grill2, do Grill: [])
- [ ] Setup Jinja2 Template for Email
- [ ] Setup Primary Bot Script

# Contributors
[Ty Chermsirivatana '27](https://github.com/WarpWing) - Initial Work

# Acknowledgements 
[Boosung Kim '25](https://github.com/boosungkim) - For his work on his own Dickinson Menu Bot which inspired this project.

[Evan Wong '24](https://github.com/evanwong1020) - For pushing me actually to create my own Bot instead of complaining.
