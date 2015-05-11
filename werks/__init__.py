"""Werks Framework - A basic Application Framework.

This is a basic and simple framework that should be reproducable in other
languages.  Provides the following:

* Service Bus (implemented in a single thread)
* Service Directory (look-up a service reference by name)

* .. more to come, surely.

"""
# Copyright 2015 Eric Gustafson
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

__version__ = '0.0.1'
__author__  = 'Eric Gustafson <eg@elfwerks.org>'



## ######################################################################

class PublishFailures(Exception):

    delimiter = '\n'

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
        self._exceptions = list()

    def capture_exception(self):
        self._exceptions.append(sys.exc_info()[1])

    def get_instances(self):
        return self._exceptions[:]

    def __str__(self):
        exception_strings = map(repr, self.get_instances())
        return self.delimiter.join(exception_strings)

    __repr__ = __str__

    def __bool__(self):
        return bool(self._exceptions)

    __nonzero__ = __bool__


## ######################################################################

class Bus(object):

    def __init__(self, **kwds):
        self.listeners = dict(
            [(channel, set()) for channel 
             in ('main')])
        super(Bus, self).__init__(**kwds)
        #print("Bus() initialized.")


    def subscribe(self, channel, callback):
        if channel not in self.listeners:
            self.listeners[channel] = set()
        self.listeners[channel].add(callback)


    def unsubscribe(self, channel, callback):
        listeners = self.listeners.get(channel)
        if listeners and callback in listeners:
            listeners.discard(callback)


    def publish(self, channel, *args, **kwargs):
        """Return the output of all subscribers in an array."""
        if channel not in self.listeners:
            return []

        exc = PublishFailures()
        output = []

        listeners = self.listeners.get(channel)
        for listener in listeners:
            try:
                output.append(listener(*args, **kwargs))
            except KeyboardInterrupt:
                raise
            except SystemExit:
                # If there were previous (non SystemExit) errors, make sure exit code in non-zero
                e = sys.exc_info()[1]
                if exc and e.code == 0:
                    e.code = 1
                # propigate SystemExit
                raise
            except:
                exc.capture_exception()
                # and continue publishing

        if exc:
            raise exc
        return output


## ######################################################################

class Registry(object):

    def __init__(self, **kwds):
        self.registry = dict()
        super(Registry, self).__init__(**kwds)


    def register(self, name, service):
        """Add 'service' with 'name' to the service registry."""
        self.services[name] = service


    def lookup(self, name, alt=None):
        """Lookup a registered service by name."""
        return self.services.get(name, alt)



## ######################################################################
## Hub classes - intended for use by application cores.
## 

class BasicHub(Registry, Bus):
    pass


class Hub(BasicHub):
    
    def __init__(self, **kwds):
        super(Hub, self).__init__(**kwds)
        #super().__init__(**kwds)




## Local Variables:
## mode: python
## End: