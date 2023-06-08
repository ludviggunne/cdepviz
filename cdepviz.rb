
require 'optparse'
require 'ostruct'
require 'pathname'

# Parse args
# TODO: Parse args
$config = OpenStruct.new
$config.dir = '.'
$config.exclude = ['example/extern']
$config.output = 'output.dot'

$EXTENSIONS = ['.c', '.h', '.cc', '.cpp', '.hpp']
$REGEX = /#include( *)("|<)(?<path>.*)("|>)/

$nodes = {}

class Node

    attr_reader :path
    attr_reader :basename
    attr_reader :connections

    def initialize(path, basename)
        @path = path
        @basename = basename
        @connections = []
    end

    def connect(node)
        @connections.push node
    end
end

def excluded(path)

    $config.exclude.each do |exclude|
        return true if /(\.\/|\/)?#{exclude}/ =~ path
    end

    return false
end

def list_files

    files = []
    Dir.glob("#{$config.dir}/**/*").each do |name|

    
    next if Pathname(name).directory?
    next if excluded(name)
        files.push name if $EXTENSIONS.include? File.extname name
    end

    return files
end

def get_includes(file)

    includes = []
    File.open(file, 'r:ISO-8859-1:utf-8').each do |line|

        match = $REGEX.match line
        includes.push match['path'] if match
    end

    return includes
end

def create_nodes

    list_files.each do |path|

        basename = Pathname(path).basename.to_s
        $nodes[basename] = $nodes[basename] || Node.new(path, basename)

        get_includes(path).each do |inc|
            
            inc_basename = Pathname(inc).basename.to_s
            $nodes[inc_basename] = $nodes[inc] || Node.new(inc, inc_basename)
            $nodes[basename].connect $nodes[inc_basename]
        end
    end
end

def output

    File.open($config.output, 'w') do |file|

        file.puts 'digraph Dependencies {'

        $nodes.each do |key, node|
            file.puts "    \"#{node.basename}\""
        end

        file.puts ''

        $nodes.each do |key, node|
            
            node.connections.each do |connection|
                file.puts "    \"#{connection.basename}\" -> \"#{node.basename}\""
            end
        end

        file.puts '}'
    end
end

create_nodes
output