nodelabel
===

Adds 2 operators with hotkey bindings for use in the node editor:

NODELABEL_OT_nodelabel

and

NODELABEL_OT_from_upstream_socket

---


### To popup a field for labeling the active node:  
ctrl+alt+shift+L

I just did not want to have to move the mouse over to the sidebar in order to label a node.  The whole point is that a hotkey presents a box where the text input already has the cursor in it.  It kind of sucks that you have to press enter twice but it gets the job done.

### To automatically label the node using the name of one of the upstream sockets it is linked to:  
ctrl+alt+shift+K

On repeated invocations, if the label of the node is already set to the name of one of the sockets it links to, then it cycles through that list of names.


