# sublime_angular_templates
Encourages you to keep your directive templates within the directive script file, to reduce congnitive load and improve efficiencey in sublime with syntax highlighting and html editing within a js file.

## Why have directive templates within the directive js file?
* Ultimately, the controller to view logic (controller function and template in a directive) is a point of constant evaluation and tweaks. This means that keeping both the template and controller logic in your own brains RAM and actual view improves understanding of the directive and development speed.
* Reduces the number of files needed for a complete directive
* Reduces the need for template caches and scripts to manage template caches
* (WARNING: OPINION) Ideally re-use of a controller across multiple views sounds like a good idea. This approach in my experience has NEVER payed off and it rarely happens in practice so there is no reason to separate a view that is used with the same controller. This opinion is somewhat backed by the changes coming in Angular 2.0 [Don't use controllers](http://teropa.info/blog/2014/10/24/how-ive-improved-my-angular-apps-by-banning-ng-controller.html)

## Alternatives for storing templates within directive files
So this plugin is a workaround to improve cognitive load, effienciency while developing, and reduction in scripts to generate final template cache files, but is not necessarily ideal. There could be many alternate solutions to expose the view with the controller while developing through other IDE plugin scripts (iOS dev in xCode provides similar features to hide and show the layouts associated with code interfaces). So keep your eyes peeled for better solutions to an important problem (cough cough... Atom).

## Usage

After setting it up, the plugin will automatically add html syntax highlighting if the following conditions are met:
* The JavaScript file ends with *.dir.js
* The template string is built as an array of strings with a join('')
```javascript
    template: [
        '<div>',
            '<h1>My Title</h1>',
            '<div class="content"></div>',
        '</div>'
    ].join('')
```

In addition to having html syntax highlighting, you can also map a keyboard shortcut to the plugin (command + T) so that you can quickly remove the quotes, escaped quotes, and commas that delimits the string in the javascript file. You can basically edit html as html and then when you save the file it will put all the delimiters back automatically.

## Careful with comments
* Comment blocks /* example */ or /** */ will cause issues in the template area, do not use them
* Single line comments should be after the template text in a line or on their own line
```javascript
    template: [
        '<div>',
            '<h1>My Title</h1>',
            '<div class="content"></div>', // this is also okay
            // this is okay too
        '</div>'
    ].join('')
```

## Installation
### First we need to install a package to help us edit a file
1. Within Sublime, install via package control 'AAAPackageDev'
2. Use shift + command + p to open the command search, and run PackageResourceViewer: Open Resource
3. Select 'JavaScript'
4. Select 'JavaScript.tmLanguage'
5. Copy this plugins 'JavaScript.tmLanguage' contents into the 'JavaScript.tmLanguage' from above

### Next we add the AngularTemplates plugin
1. In Sublime, go to Tools > New Plugin
2. Copy the text from this plugins 'AngularTemplates.py' file into your new plugin file
3. Save the new plugin as 'AngularTemplates.py'

### Last we map the new plugin to a keyboard shortcut
9. In Sublime go to Preferences > Key Bindings - User and add this line
```json
{ "keys": ["super+t"], "command": "angular_templates_transform" }
```

That should complete the install. Now you should see html template strings within Angular directive files (*.dir.js) being highlighted as html. Additionally, if you hit your keyboard shortcut you can remove all the string related delimeters and when you save the file they will be put back automatically.
