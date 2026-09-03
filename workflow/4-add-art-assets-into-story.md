# WORKFLOW PROCESS #4 - Add Art Assets Into Story

1) Prompt me to specify the name of the finalized story pitch within the REPO_ROOT/pitches/finalized folder location, and await my response.

2) Use the name of the story to reference the assets-manifest.md file within the REPO_ROOT/{project_name} folder location.

3) Check if every listed image exists within the same REPO_ROOT/{project_name}/assets/image folder location. If yes, continue. Otherwise, stop here and break execution and inform what images are still missing.

4) Modify the REPO_ROOT/{project_name}/{project_name}.html file, so that every passage has the correct actor/actress image as specified in the assets-manifest.md file:

Insert at the beginning of each correct passage (tw-passage):

<div id="actress" class="align-m"><img width="512" height="512" class="align-m" src="assets/image/{image-name}.png" /></div>
