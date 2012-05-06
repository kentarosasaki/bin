#!/usr/local/bin/ruby

# -*- coding: UTF-8 -*-

require 'yaml'
require 'logger'

class Glsync

  def initialize
    logger_config
    read_config
  end

  def logger_config
    @rsync_log = Logger.new('/Users/kentaro/bin/rsync.log', 7)
    @rsync_log.level = Logger::INFO
    @delete_log = Logger.new('/Users/kentaro/bin/delete.log', 7)
    @delete_log.level = Logger::INFO
  end

  def read_config
    yaml = {}
    file = File::basename('/Users/kentaro/bin/glsync.yaml')
    yaml = YAML::load(File.open(file)) if File.exists? file
    @rsync_args = yaml['rsync'] or ''
    @mappings = yaml['mappings'] or {}
  end

  def get_rsync_args
    rsync_args = @rsync_args + ' '
    return rsync_args
  end

  def check_end_with(mapping)
    if mapping.end_with? "\/"
      return mapping
    else
      return mapping + "\/"
    end
  end

  def check_dir_exist(directory)
    begin
      dest = open("| ls #{directory}")
    rescue
      Dir::mkdir("#{directory}")
      retry
      @rsync_log.error($!)
    else
      dest.close
    end    
  end
  
  def mapping_loop(command)
    path = {}
    rsync_args = get_rsync_args
    if command == "rsync"
      @rsync_log.info("rsync started")
    elsif command == "delete"
      @delete_log.info("deletion started")
    end
    @mappings.each_pair do |key, value|
      path[:src] = check_end_with(key)
      path[:dest] = check_end_with(value)
      check_dir_exist(path[:dest])
      if command == "rsync"
        @rsync_log.info("pushing #{path[:src]} to #{path[:dest]} with options #{rsync_args}")
        unless system("rsync \"#{path[:src]}\" \"#{path[:dest]}\" #{rsync_args}")
          @rsync_log.error("rsync failed: src = #{path[:src]}, dest = #{path[:dest]}")
        end
      elsif command == "delete"
        @delete_log.info("delete 90 days' data in #{path[:dest]}")
        system("find \"#{path[:dest]}\" -mtime +90 -type f -print0 | xargs -0 rm -f") rescue false
      end
    end
  end    
  
end
