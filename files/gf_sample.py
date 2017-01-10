#!/usr/bin/env python

"""Do some stuff on the specified firewall:

* Connect
* List out the AddressObjects defined
* Create AddressObject "ivan" if it doesn't exist
* Create a SecurityPolicy that allows L3-trust/ivan to goto L3-untrust/any
"""


import pandevice
import pandevice.firewall
import pandevice.objects
import pandevice.policies


def main():
    # Creates the firewall object
    fw = pandevice.firewall.Firewall('10.5.172.187', 'admin', 'paloalto')

    # Doing anything on the firewall will login to it, you can skip this
    # step if you want.
    fw.refresh_system_info()

    # Get the list of address objects from the firewall.  All objects that
    # pandevice knows of can be retrieved by doing this:
    #   <object>.refreshall(<parent>)
    # In this case, AddressObjects are children of the firewall, so we pass
    # in the firewall as the parent.  Besides returning a list of the answers,
    # the children are added to the parent that you've passed in.
    addresses = pandevice.objects.AddressObject.refreshall(fw)
    print 'Found {0} address(es)'.format(len(addresses))
    for x in addresses:
        print ' - {0}'.format(x.name)
    if addresses:
        print

    # Here we show both object updates and creation, depending on what we
    # found when we queried the live device.  If the "ivan" AO exists *and*
    # the type is 'ip-netmask', then reverse the IP octets.  If "ivan" exists
    # but isn't an 'ip-netmask', then leave it alone.  Finally, if it doesn't
    # exist, then create it.
    for ao in addresses:
        if ao.name == 'ivan':
            if ao.type != 'ip-netmask':
                print 'Leaving non-ip-netmask "ivan" alone'
            else:
                print 'Reversing "ivan" IP octet'
                ao.value = '.'.join(reversed(ao.value.split('.')))
                print 'Applying: {0}'.format(ao.apply())
            break
    else:
        print 'AddressObject "ivan" not present, creating it'
        ao = pandevice.objects.AddressObject('ivan', '10.20.30.40')
        fw.add(ao)
        print 'Creating: {0}'.format(ao.create())

    # All rules (Security, NAT, etc) are children of Rulebase in the
    # PANOS spec.  So we need to get Rulebase from the firewall.
    rule_base = pandevice.policies.Rulebase.refreshall(fw)
    if rule_base:
        # The `refreshall()` functions always return a list, and since I think
        # there is only every one Rulebase, I just update my variable to be the
        # one Rulebase object before moving on.
        rule_base = rule_base[0]

        # You'll notice I don't do any `refreshall()` to get the SecurityRules
        # at this point.  This is because if you do `refreshall()` on a parent,
        # all of it's children are returned in the XML.  So those additional
        # children are already part of the Rulebase object, we just need to
        # find them (if any exist).
        security_rules = rule_base.findall(pandevice.policies.SecurityRule)
        print 'Found {0} security rule(s)'.format(len(security_rules))
        for rule in security_rules:
            print ' - {0}'.format(rule.name)
        if security_rules:
            print

        # Just like last time, we do some modify stuff if it exists, otherwise
        # we will create it.
        target_rule = 'allow ivan to do stuff'
        for rule in security_rules:
            if rule.name == target_rule:
                if rule.source == 'any':
                    print 'Togging {0} source to "ivan"'
                    rule.source = 'ivan'
                else:
                    print 'Toggling {0} source to "any"'
                    rule.source = 'any'
                print 'Applying: {0}'.format(rule.apply())
                break
        else:
            print 'Rule "{0}" doesn\'t exist, creating'.format(target_rule)
            rule = pandevice.policies.SecurityRule(
                name=target_rule,
                source='ivan',
                fromzone='L3-trust',
                tozone='L3-untrust',
                action='allow')
            rule_base.add(rule)
            print 'Creating: {0}'.format(rule.create())
            print 'Done!'
    else:
        print 'No Rulebase present...'

    # Commit the changes.  The `sync` flag is effectively "block until the sync
    # is done."  The default behavior is not to wait.
    print 'Committing result...'
    print 'Result: {0}'.format(fw.commit(sync=True))


if __name__ == '__main__':
    main()
