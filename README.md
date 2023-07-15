# Welcome to  AO Labs

We're building the next layer in the AI stack, AI trained by local context, awareness as code. More on our website.

At these earliest of stages our AI is at a very basic level of self-association, comparable to simplest of animals. It's not ChatGPT or anywhere near human levels, but it has qualities that LLMs and other status quo AI lack.

This *archs repo* contains our first agent configurations and their applications, all open-source. 
- [Arch class](https://github.com/aolabsai/archs/blob/main/Arch.py)
- [Agent Archs](https://github.com/aolabsai/archs/tree/main/Architectures)
- [Applications](https://github.com/aolabsai/archs/tree/main/Applications)
	- Hello, World-- our Clam-level AGI and simplest reference design     [[try demo](https://aolabs.streamlit.app/)] [[view code](https://github.com/aolabsai/archs/tree/main/Applications/HelloWorld-BasicClam)]
	- Netbox- Device Discovery-- an Agent as a context-aware autocomplete for relational data, applied to Netbox for network automation     [[try demo](https://aolabs-netbox.streamlit.app/)] [[view code](https://github.com/aolabsai/archs/tree/main/Applications/Netbox/Device_Discovery)]
- [WIP Applications](https://github.com/aolabsai/archs/tree/main/WIP%20Architectures)-- many more coming soon!
- [API OAS 3 Definition](https://github.com/aolabsai/archs/blob/main/core_api.yaml)-- details of the Agents-as-a-Service API provided as a playground and Agent hosting/deployment service

---
## RE Licensing: Open Source & Our API

Everything in the **archs** repo is open-source: the **Arch** class, particular Agents' archs, and associated applications. We hope this inspires more use-cases as we're fresh from the lab.

We plan to open-source the rest of our code progressively over time, that is, the **Agent** class and code that constructs an Agent given an Arch, and this is an evolving discussion as we're careful to ensure we make the right decisions now to realize the long-term potential we've seen with this code. We had started this journey as researchers after all, so there are years of context to be shared.

Our Agents-as-a-Service API is our **Core**'s **Agent** class running on AWS, as a playground to spin up and test Agents without having to install anything, so that you also don't have to worry about hosting multiple unique Agents for your users. However, our Agents are designed to be run directly at the edge.
- If you are interested in joining us as a Core Contributor, please email Ali or say hi on Slack or our other channels.
- If you are interested in running Agents locally and need access to Core now, please reach out. joining us as a core contributor contributing to our code code, please say hi on slack 

###
More resources:
- View a [Visual Representation of archs and applications])(https://miro.com/app/board/uXjVM_kESvI=/?share_link_id=686677372269) on Miro
- Our docs and API reference on [docs.aolabs.ai](https://docs.aolabs.ai)
- Our [discord](https://discord.gg/Zg9bHPYss5)


Thank you very much for being here. We welcome contributors of all levels, on the application layer or with our **Core** work.