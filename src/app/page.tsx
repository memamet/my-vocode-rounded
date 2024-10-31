/* eslint-disable react/no-unescaped-entities */
"use client";

export const runtime = "edge";

import dynamic from "next/dynamic";
import Image from "next/image";

const VocodeAppDynamic = dynamic(() => import("@/components/vocode-app"), {
  ssr: false,
});

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="flex justify-end">
        <a
          href="https://rounded.com/contact"
          target="_blank"
          rel="noopener noreferrer"
          className="p-4"
        >
          <Image
            src="/rounded_logo.svg"
            alt="Rounded Logo"
            width={100}
            height={24}
            priority
          />
        </a>
      </div>
      <div className="relative flex place-items-center z-[-1]">
        <Image
          className="relative "
          src="/donny_logo.avif"
          alt="Donny, the Rounded AI Assistant"
          width={280}
          height={37}
          priority
        />
      </div>
      <h1 className="text-3xl font-semibold text-center dark:text-white my-8">
        Meet Donny – Your Expert Guide to Rounded
      </h1>
      <p className="text-lg text-center font-semibold dark:text-white mb-8">
        Donny is here to help you learn everything about Rounded's journey,
        products, and innovations.
      </p>
      <div className="flex flex-col items-center justify-center py-4">
        <VocodeAppDynamic
          defaultBackendUrl={
            (window.location.protocol === "https:" ? "wss:" : "ws:") +
            "//" +
            window.location.host +
            "/api/python/conversation"
          }
          isInputEditable={false}
        />
      </div>
      <div className="grid text-center lg:max-w-5xl lg:w-full lg:grid-cols-4 lg:text-left gap-4">
        <div>
          <h2 className="text-2xl font-bold dark:text-white mb-4">
            About Rounded
          </h2>
          <p className="text-md dark:text-white">
            Rounded was founded to transform customer interactions with
            AI-driven callbots, starting in healthcare. From patient scheduling
            to scalable voice solutions, Rounded is building the future of
            automated customer service.
          </p>
        </div>
        <div>
          <h2 className="text-2xl font-bold dark:text-white mb-4">
            Our Founders
          </h2>
          <p className="text-md dark:text-white">
            Rounded was created by Aymeric Vaudelin, Valentin Flageat, and
            Yassine M'hamdi, who met at the X-HEC Entrepreneurs program. Their
            mission: to make customer interactions more efficient, scalable, and
            engaging.
          </p>
        </div>
        <div>
          <h2 className="text-2xl font-bold dark:text-white mb-4">
            Voice Agent Factory
          </h2>
          <p className="text-md dark:text-white">
            The Voice Agent Factory is Rounded’s flagship tool, enabling
            companies to build custom AI voice agents that seamlessly integrate
            with business operations, no matter the industry.
          </p>
        </div>
        <div>
          <h2 className="text-2xl font-bold dark:text-white mb-4">
            International Growth
          </h2>
          <p className="text-md dark:text-white">
            Rounded has expanded globally, with support from programs like
            Skydeck (California) and Station F (France), bringing innovative
            voice solutions to customers worldwide.
          </p>
        </div>
      </div>
    </main>
  );
}
