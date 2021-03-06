import importlib.util
import config
import os

components=dict()

class SubComponentsNotAllowed(Exception):
    pass

class BaseCompoment(object):
    version="0.0.1alpha"
    author="Bob Smith"
    name="Abstarct1"
    description="Amazing component"
    subcomponents=dict()
    ALLOW_SUBCOMPONETNS=False
    def __init__(self,parent,name,app,*args,**kwargs):#FIXED:Issue #7
        self.args=args
        self.kwargs=kwargs
        self.parent=parent
        self.name=name
        self.app=app

    def event_tosubs(self,event):#DO NOT DELETE:FIX for ISSUE #1.
        """Do not modificate this method!!!
           This method giving evet to all subcomponents of component."""
        config.log.log(str(self.subcomponents))
        if self.ALLOW_SUBCOMPONETNS:
            for key in self.subcomponents:
                if key==self.name:
                   break
                config.log.log("C/%s/I:Sending event to %s"%(self.name,key))
                self.subcomponents[key].on_event(event)
                self.subcomponents[key].event_tosubs(event)

    def on_event(self,event):
        pass

    def on_create(self):
        pass

    def add_component(self,component,name,*args,**kwargs):
        """adds compnent to plugin
           component--component name from components
           name--new unique name of component
           Will raise exception if subcomponents are not allowed!!!"""
        if self.ALLOW_SUBCOMPONETNS:
          _component=components[component](self,name,self.app,*args,**kwargs)
          self.subcomponents.update({name:_component})
          self.subcomponents[name].on_create()
        else:
          raise SubComponentsNotAllowed("Subcomponents are not allowed in "+self.name)


def load_component(path,name):
    """loads compnent from specified path
       path--path to compnent"""
    if not os.path.isfile(path):
        config.log.log("Will not load component from "+path+"becauese file not exists!")
        return
    mod=importlib.util.spec_from_file_location(name,path)#importing compnent
    component=importlib.util.module_from_spec(mod)
    mod.loader.exec_module(component)
    components[component.name]=component.MainComponent
    config.log.log(component.name+" loaded")#logging that new component succesfully loaded
