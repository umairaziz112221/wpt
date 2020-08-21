// Responds to onmessage events from other frames to check for pending input.
onmessage = async e => {
  if (e.data !== 'check-input') return;

  const discreteOptions = new IsInputPendingOptions({ includeContinuous: false });
  const continuousOptions = new IsInputPendingOptions({ includeContinuous: true });

  // Use a reasonable time to wait after dispatching events, since we want to be
  // able to test for cases where isInputPending returns false.
  const DISPATCH_WAIT_TIME_MS = 200;

  // Wait a reasonable amount of time for the event to be enqueued.
  for (const end = performance.now() + DISPATCH_WAIT_TIME_MS; performance.now() < end;) {}

  const hasDiscrete = navigator.scheduling.isInputPending(discreteOptions);
  const hasContinuous = navigator.scheduling.isInputPending(continuousOptions);

  e.source.postMessage({
    discrete: hasDiscrete,
    continuous: hasContinuous,
  }, '*');
}
