using Mutagen.Bethesda;
using Mutagen.Bethesda.Pex;

if (args.Length != 1)
{
    Console.Error.WriteLine("usage: PexContractProbe <NiOverride.pex>");
    return 2;
}

var path = Path.GetFullPath(args[0]);
var pex = PexFile.CreateFromFile(path, GameCategory.Skyrim);
var functions = pex.Objects
    .SelectMany(obj => obj.States)
    .SelectMany(state => state.Functions)
    .ToList();
var stateEvents = functions
    .Where(function => function.FunctionName is "onBeginState" or "onEndState")
    .ToList();
var ordinaryFunctions = functions.Except(stateEvents).ToList();
var target = functions
    .Where(function => function.FunctionName == "GetNodeTransformScaleMode")
    .ToList();

if (pex.Objects.Count != 1)
    throw new InvalidDataException($"object count {pex.Objects.Count} != 1");
if (pex.Objects.Single().States.Count != 1)
    throw new InvalidDataException($"state count {pex.Objects.Single().States.Count} != 1");
if (ordinaryFunctions.Count != 183 || stateEvents.Count != 2 || functions.Count != 185)
    throw new InvalidDataException(
        $"callable contract differs: functions={ordinaryFunctions.Count} " +
        $"state_events={stateEvents.Count} total={functions.Count}");
if (target.Count != 1)
    throw new InvalidDataException($"target function count {target.Count} != 1");
if (target.Single().Function.ReturnTypeName != "Int")
    throw new InvalidDataException(
        $"target return type {target.Single().Function.ReturnTypeName} != Int");
if (new FileInfo(path).Length != 12_935)
    throw new InvalidDataException($"file size {new FileInfo(path).Length} != 12935");

Console.WriteLine(
    "PASS Mutagen parse: objects=1 states=1 functions=183 state_events=2 total=185 " +
    "GetNodeTransformScaleMode.count=1 return=Int size=12935");
return 0;
